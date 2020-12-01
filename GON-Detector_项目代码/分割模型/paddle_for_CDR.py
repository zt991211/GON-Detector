import cv2
import random
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
from paddle import fluid
from paddle.fluid.dygraph.nn import Conv2D, BatchNorm, Pool2D, Conv2DTranspose
from skimage.transform import rotate, resize


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


train_img_path = '/home/aistudio/work/train-images/'
label_path = '/home/aistudio/work/labels/'
valid_img_path = '/home/aistudio/work/valid-images/'


# 对读入的图像数据进行预处理
def transform_img(img, flag=0):
    # 将图片尺寸缩放道 400*400
    img = cv2.resize(img, (400, 400))
    # 读入的图像数据格式是[H, W, C]
    # 使用转置操作将其变成[C, H, W]
    img = np.transpose(img, (2, 0, 1)).astype('float32')
    # 将数据范围调整到[0.0, 1.0]之间
    if flag == 1:
        img = img / 255.
    return img


def getCDR(img):
    height = img.shape[0]
    width = img.shape[1]
    h_first = 0
    h_end = 0
    w_first = 0
    w_end = 0
    for i in range(height):
        if sum(img[i, :]) >= 1:
            h_first = i
            break
    for i in range(height):
        if sum(img[i, :]) >= 1:
            h_end = i
    h = abs(h_first - h_end)
    for i in range(width):
        if sum(img[:, i]) >= 1:
            w_first = i
            break
    for i in range(width):
        if sum(img[:, i]) >= 1:
            w_end = i
    w = abs(w_first - w_end)
    return h, w


# 定义训练集数据读取器
def data_loader(datadir, labeldir, batch_size=10):
    # 将datadir目录下的文件列出来，每条文件都要读入
    filenames = os.listdir(datadir)

    def reader():
        random.shuffle(filenames)
        batch_imgs = []
        batch_labels = []
        for name in filenames:
            filepath = os.path.join(datadir, name)
            labelpath = os.path.join(labeldir, name)
            img = transform_img(np.array(Image.open(filepath)))
            label = transform_img(np.array(Image.open(labelpath)), 1)
            batch_imgs.append(img)
            batch_labels.append(label)
            if len(batch_imgs) == batch_size:
                # 当数据列表的长度等于batch_size的时候，
                # 把这些数据当作一个mini-batch，并作为数据生成器的一个输出
                imgs_array = np.array(batch_imgs).astype('float32')
                labels_array = np.array(batch_labels).astype('float32')
                yield imgs_array, labels_array
                batch_imgs = []
                batch_labels = []

    return reader


def dice_loss2(y_pred, y_true):
    smooth = 1.
    # print(y_true.shape)
    y_true_f = fluid.layers.flatten(y_true, 3)  # 将 y_true 拉伸为一维.
    # print(y_true_f.shape)
    y_pred_f = fluid.layers.flatten(y_pred, 3)
    y_true_f = fluid.layers.reshape(y_true_f, [y_true_f.shape[0]])
    y_pred_f = fluid.layers.reshape(y_pred_f, [y_pred_f.shape[0]])
    intersection = fluid.layers.reduce_sum(y_true_f * y_pred_f)
    # 训练要除以8
    return 1. - (2. * intersection + smooth) / (
                fluid.layers.reduce_sum(y_true_f) + fluid.layers.reduce_sum(y_pred_f) + smooth)


# 定义训练过程
def train(model):
    model_state_dict, _ = fluid.load_dygraph('/home/aistudio/work/mnet_8size.pdparams')
    model.load_dict(model_state_dict)
    with fluid.dygraph.guard():
        print('start training ... ')
        model.train()
        epoch_num = 50
        # 定义优化器
        opt = fluid.optimizer.AdamOptimizer(parameter_list=model.parameters())
        # 定义数据读取器，训练数据读取器和验证数据读取器
        train_loader = data_loader(train_img_path, label_path, batch_size=8)
        valid_loader = data_loader(valid_img_path, label_path, batch_size=8)
        train_losses = []
        val_losses = []
        epoch_x = []
        train_loss = 0.0
        val_loss = 0.0
        for epoch in range(epoch_num):
            train_loss = 0.0
            val_loss = 0.0
            for batch_id, data in enumerate(train_loader()):
                x_data, y_data = data
                img = fluid.dygraph.to_variable(x_data)
                label = fluid.dygraph.to_variable(y_data)
                # 运行模型前向计算，得到预测值
                out6, out7, out8, out9, out10 = model(img)
                # 进行loss计算
                loss6 = dice_loss2(out6[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out6[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss7 = dice_loss2(out7[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out7[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss8 = dice_loss2(out8[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out8[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss9 = dice_loss2(out9[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out9[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss10 = dice_loss2(out10[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out10[:, 1, :, :],
                                                                                             label[:, 1, :, :]) * 0.5
                loss = (loss6 + loss7 + loss8 + loss9) * 0.1 + loss10 * 0.6
                avg_loss = fluid.layers.mean(loss)
                train_loss += avg_loss
                # 反向传播，更新权重，清除梯度
                avg_loss.backward()
                opt.minimize(avg_loss)
                model.clear_gradients()
            train_losses.append(train_loss.numpy())

            model.eval()
            for batch_id, data in enumerate(valid_loader()):
                x_data, y_data = data
                img = fluid.dygraph.to_variable(x_data)
                label = fluid.dygraph.to_variable(y_data)
                # 运行模型前向计算，得到预测值
                out6, out7, out8, out9, out10 = model(img)
                # 进行loss计算
                loss6 = dice_loss2(out6[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out6[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss7 = dice_loss2(out7[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out7[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss8 = dice_loss2(out8[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out8[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss9 = dice_loss2(out9[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out9[:, 1, :, :],
                                                                                           label[:, 1, :, :]) * 0.5
                loss10 = dice_loss2(out10[:, 0, :, :], label[:, 0, :, :]) * 0.5 + dice_loss2(out10[:, 1, :, :],
                                                                                             label[:, 1, :, :]) * 0.5
                loss = (loss6 + loss7 + loss8 + loss9) * 0.1 + loss10 * 0.6
                avg_loss = fluid.layers.mean(loss)
                val_loss += avg_loss
            val_losses.append(val_loss.numpy())
            model.train()
            epoch_x.append(epoch + 1)
            print(
                'epoch is {}, train loss is {}, val loss is {}'.format(epoch + 1, train_loss.numpy(), val_loss.numpy()))
            if (epoch + 1) % 10 == 0:
                fluid.save_dygraph(model.state_dict(), '/home/aistudio/work/mnet' + str(epoch + 1))
        plt.plot(epoch_x, train_losses, color='r')
        plt.plot(epoch_x, val_losses, color='blue')
        plt.savefig('/home/aistudio/work/loss.jpg')
        plt.show()
        # save params of model
        fluid.save_dygraph(model.state_dict(), '/home/aistudio/work/mnet')
        # save optimizer state
        fluid.save_dygraph(opt.state_dict(), '/home/aistudio/work/mnet')


if __name__ == '__main__':
    # 创建模型
    with fluid.dygraph.guard():
        model = M_net()
        # 启动训练过程
        # train(model)
        # 测试模型效果

        DiscROI_size=600
        model_state_dict, _ = fluid.load_dygraph('model_weights/mnet30.pdparams')
        model.load_dict(model_state_dict)
        model.eval()
        img=[]
        img.append(transform_img(np.array(Image.open('test_img/V0001_0.png'))))
        img = np.array(img)
        img = fluid.dygraph.to_variable(img)
        out6, out7, out8, out9, out10 = model(img)
        out10 = out10.numpy()
        out10 = np.reshape(out10,(out10.shape[1],out10.shape[2],out10.shape[3]))
        out10 = np.transpose(out10, (1,2,0))
        disc_map = np.array(Image.fromarray(out10[:, :, 0]).resize((600, 600)))
        cup_map = np.array(Image.fromarray(out10[:, :, 1]).resize((600, 600)))
        disc_map[-round(DiscROI_size / 3):, :] = 0
        cup_map[-round(DiscROI_size / 2):, :] = 0
        De_disc_map = cv2.linearPolar(rotate(disc_map, 90), (DiscROI_size / 2, DiscROI_size / 2),
                                  DiscROI_size / 2, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)
        De_cup_map = cv2.linearPolar(rotate(cup_map, 90), (DiscROI_size / 2, DiscROI_size / 2),
                                 DiscROI_size / 2, cv2.WARP_FILL_OUTLIERS + cv2.WARP_INVERSE_MAP)
        ret,De_cup_map=cv2.threshold(De_cup_map,0.5,1,cv2.THRESH_BINARY)
        res,De_disc_map=cv2.threshold(De_disc_map,0.5,1,cv2.THRESH_BINARY)


        # calculate CDR

        disc_h,disc_w=getCDR(De_disc_map)
        cup_h,cup_w=getCDR(De_cup_map)

        print('垂直CDR的值为:'+str(cup_h*1.00/disc_h))
        print('水平CDR的值为:'+str(cup_w*1.00/disc_w))


        # 评估模型指标
        '''
        model.eval()
        test_loader = data_loader(valid_img_path,label_path, batch_size=1)
        tot_loss=0.0
        for batch_id, data in enumerate(test_loader()):
                x_data, y_data = data
                img = fluid.dygraph.to_variable(x_data)
                label = fluid.dygraph.to_variable(y_data)
                # 运行模型前向计算，得到预测值
                out6, out7, out8, out9, out10 = model(img)
                loss6 = dice_loss2(out6[:,0,:,:],label[:,0,:,:])*0.5+dice_loss2(out6[:,1,:,:],label[:,1,:,:])*0.5
                loss7 = dice_loss2(out7[:, 0, :, :], label[:, 0, :, :])*0.5+dice_loss2(out7[:, 1, :, :], label[:, 1, :, :])*0.5
                loss8 = dice_loss2(out8[:, 0, :, :], label[:, 0, :, :])*0.5+dice_loss2(out8[:, 1, :, :], label[:, 1, :, :])*0.5
                loss9 = dice_loss2(out9[:, 0, :, :], label[:, 0, :, :])*0.5+dice_loss2(out9[:, 1, :, :], label[:, 1, :, :])*0.5
                loss10 = dice_loss2(out10[:, 0, :, :], label[:, 0, :, :])*0.5+dice_loss2(out10[:, 1, :, :], label[:, 1, :, :])*0.5
                loss = (loss6+loss7+loss8+loss9)*0.1+loss10*0.6
                avg_loss = fluid.layers.mean(loss)
                tot_loss+=avg_loss
        print(tot_loss/1200.)
        '''



