from paddle import fluid
from paddle.fluid.dygraph.nn import Conv2D, BatchNorm, Pool2D, Conv2DTranspose

class Conv_Block(fluid.dygraph.Layer):
    def __init__(self, inc, outc, size, padding=1):
        super(Conv_Block, self).__init__()
        self.c1 = Conv2D(num_channels=inc, num_filters=outc, filter_size=size, padding=padding)
        self.bn = BatchNorm(num_channels=outc, act='relu', in_place=True)

    def forward(self, x):
        x = self.c1(x)
        x = self.bn(x)
        return x


class M_net(fluid.dygraph.Layer):
    def __init__(self):
        super(M_net, self).__init__()
        self.scale1 = Pool2D(pool_size=2, pool_type='avg', pool_stride=2, pool_padding=0)
        self.scale2 = Pool2D(pool_size=2, pool_type='avg', pool_stride=2, pool_padding=0)
        self.scale3 = Pool2D(pool_size=2, pool_type='avg', pool_stride=2, pool_padding=0)

        self.block1_conv1 = Conv_Block(3, 32, 3, 1)
        self.block1_conv2 = Conv_Block(32, 32, 3, 1)
        self.block1_pool1 = Pool2D(pool_size=2, pool_type='max', pool_stride=2, pool_padding=0)

        self.block2_input1 = Conv_Block(3, 64, 3, 1)
        self.block2_conv1 = Conv_Block(96, 64, 3, 1)
        self.block2_conv2 = Conv_Block(64, 64, 3, 1)
        self.block2_pool1 = Pool2D(pool_size=2, pool_type='max', pool_stride=2, pool_padding=0)

        self.block3_input1 = Conv_Block(3, 128, 3, 1)
        self.block3_conv1 = Conv_Block(192, 128, 3, 1)
        self.block3_conv2 = Conv_Block(128, 128, 3, 1)
        self.block3_pool1 = Pool2D(pool_size=2, pool_type='max', pool_stride=2, pool_padding=0)

        self.block4_input1 = Conv_Block(3, 256, 3, 1)
        self.block4_conv1 = Conv_Block(384, 256, 3, 1)
        self.block4_conv2 = Conv_Block(256, 256, 3, 1)
        self.block4_pool1 = Pool2D(pool_size=2, pool_type='max', pool_stride=2, pool_padding=0)

        self.block5_conv1 = Conv_Block(256, 512, 3, 1)
        self.block5_conv2 = Conv_Block(512, 512, 3, 1)

        self.block6_dconv = Conv2DTranspose(512, 256, 2, stride=2)
        self.block6_conv1 = Conv_Block(512, 256, 3, 1)
        self.block6_conv2 = Conv_Block(256, 256, 3, 1)

        self.block7_dconv = Conv2DTranspose(256, 128, 2, stride=2)
        self.block7_conv1 = Conv_Block(256, 128, 3, 1)
        self.block7_conv2 = Conv_Block(128, 128, 3, 1)

        self.block8_dconv = Conv2DTranspose(128, 64, 2, stride=2)
        self.block8_conv1 = Conv_Block(128, 64, 3, 1)
        self.block8_conv2 = Conv_Block(64, 64, 3, 1)

        self.block9_dconv = Conv2DTranspose(64, 32, 2, stride=2)
        self.block9_conv1 = Conv_Block(64, 32, 3, 1)
        self.block9_conv2 = Conv_Block(32, 32, 3, 1)

        self.side63 = Conv2D(256, 2, 1, act='sigmoid')
        self.side73 = Conv2D(128, 2, 1, act='sigmoid')
        self.side83 = Conv2D(64, 2, 1, act='sigmoid')
        self.side93 = Conv2D(32, 2, 1, act='sigmoid')

    def forward(self, x):
        scale_img_1 = self.scale1(x)
        scale_img_2 = self.scale2(scale_img_1)
        scale_img_3 = self.scale3(scale_img_2)

        conv1 = self.block1_conv1(x)
        conv1 = self.block1_conv2(conv1)
        pool1 = self.block1_pool1(conv1)

        input2 = self.block2_input1(scale_img_1)
        input2 = fluid.layers.concat([input2, pool1], axis=1)
        conv2 = self.block2_conv1(input2)
        conv2 = self.block2_conv2(conv2)
        pool2 = self.block2_pool1(conv2)

        input3 = self.block3_input1(scale_img_2)
        input3 = fluid.layers.concat([input3, pool2], axis=1)
        conv3 = self.block3_conv1(input3)
        conv3 = self.block3_conv2(conv3)
        pool3 = self.block3_pool1(conv3)

        input4 = self.block4_input1(scale_img_3)
        input4 = fluid.layers.concat([input4, pool3], axis=1)
        conv4 = self.block4_conv1(input4)
        conv4 = self.block4_conv2(conv4)
        pool4 = self.block4_pool1(conv4)

        conv5 = self.block5_conv1(pool4)
        conv5 = self.block5_conv2(conv5)

        temp6 = self.block6_dconv(conv5)
        up6 = fluid.layers.concat([temp6, conv4], axis=1)
        conv6 = self.block6_conv1(up6)
        conv6 = self.block6_conv2(conv6)

        temp7 = self.block7_dconv(conv6)
        up7 = fluid.layers.concat([temp7, conv3], axis=1)
        conv7 = self.block7_conv1(up7)
        conv7 = self.block7_conv2(conv7)

        temp8 = self.block8_dconv(conv7)
        up8 = fluid.layers.concat([temp8, conv2], axis=1)
        conv8 = self.block8_conv1(up8)
        conv8 = self.block8_conv2(conv8)

        temp9 = self.block9_dconv(conv8)
        up9 = fluid.layers.concat([temp9, conv1], axis=1)
        conv9 = self.block9_conv1(up9)
        conv9 = self.block9_conv2(conv9)

        side6 = fluid.layers.resize_nearest(conv6, scale=8)
        side7 = fluid.layers.resize_nearest(conv7, scale=4)
        side8 = fluid.layers.resize_nearest(conv8, scale=2)

        out6 = self.side63(side6)
        out7 = self.side73(side7)
        out8 = self.side83(side8)
        out9 = self.side93(conv9)
        out10 = (out6 + out7 + out8 + out9) / 4

        return out6, out7, out8, out9, out10
