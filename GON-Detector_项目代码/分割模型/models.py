import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Dropout, Flatten, Dense, \
    AveragePooling2D, concatenate, Conv2DTranspose, UpSampling2D, Input,average

# small conv block
class Conv_Block(Model):
    """docstring for Conv_Block"""

    def __init__(self, fliters, kernel_size, padding_name, activation_name):
        super(Conv_Block, self).__init__()
        self.process = tf.keras.models.Sequential([
            Conv2D(fliters, (kernel_size, kernel_size), padding=padding_name),
            BatchNormalization(),
            Activation(activation_name),
        ])

    def call(self, x):
        x = self.process(x)
        return x;

class Mnet(Model):

    def __init__(self):
        super(Mnet, self).__init__()

        self.scale1 = AveragePooling2D(pool_size=(2, 2))
        self.scale2 = AveragePooling2D(pool_size=(2, 2))
        self.scale3 = AveragePooling2D(pool_size=(2, 2))

        self.block1_conv1 = Conv_Block(32, 3, 'same', 'relu')
        self.block1_conv2 = Conv_Block(32, 3, 'same', 'relu')
        self.block1_pool1 = MaxPool2D(pool_size=(2, 2))

        self.block2_input1 = Conv_Block(64, 3, 'same', 'relu')
        self.block2_conv1 = Conv_Block(64, 3, 'same', 'relu')

        self.block2_conv2 = Conv_Block(64, 3, 'same', 'relu')
        self.block2_pool1 = MaxPool2D(pool_size=(2, 2))

        self.block3_input1 = Conv_Block(128, 3, 'same', 'relu')
        self.block3_conv1 = Conv_Block(128, 3, 'same', 'relu')
        self.block3_conv2 = Conv_Block(128, 3, 'same', 'relu')
        self.block3_pool1 = MaxPool2D(pool_size=(2, 2))

        self.block4_input1 = Conv_Block(256, 3, 'same', 'relu')
        self.block4_conv1 = Conv_Block(256, 3, 'same', 'relu')
        self.block4_conv2 = Conv_Block(256, 3, 'same', 'relu')
        self.block4_pool1 = MaxPool2D(pool_size=(2, 2))

        self.block5_conv1 = Conv_Block(512, 3, 'same', 'relu')
        self.block5_conv2 = Conv_Block(512, 3, 'same', 'relu')

        self.block6_dconv = Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same')
        self.block6_conv1 = Conv_Block(256, 3, 'same', 'relu')
        self.block6_conv2 = Conv_Block(256, 3, 'same', 'relu')

        self.block7_dconv = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')
        self.block7_conv1 = Conv_Block(128, 3, 'same', 'relu')
        self.block7_conv2 = Conv_Block(128, 3, 'same', 'relu')

        self.block8_dconv = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')
        self.block8_conv1 = Conv_Block(64, 3, 'same', 'relu')
        self.block8_conv2 = Conv_Block(64, 3, 'same', 'relu')

        self.block9_dconv = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')
        self.block9_conv1 = Conv_Block(32, 3, 'same', 'relu')
        self.block9_conv2 = Conv_Block(32, 3, 'same', 'relu')

        self.side63 = Conv_Block(2, 1, 'valid', 'sigmoid')
        self.side73 = Conv_Block(2, 1, 'valid', 'sigmoid')
        self.side83 = Conv_Block(2, 1, 'valid', 'sigmoid')
        self.side93 = Conv_Block(2, 1, 'valid', 'sigmoid')

    def call(self, x):

        # three scale imgs
        scale_img_1 = self.scale1(x)
        scale_img_2 = self.scale2(scale_img_1)
        scale_img_3 = self.scale3(scale_img_2)

        conv1 = self.block1_conv1(x)
        conv1 = self.block1_conv2(conv1)
        pool1 = self.block1_pool1(conv1)

        input2 = self.block2_input1(scale_img_1)
        input2 = tf.concat([input2, pool1], axis=3)
        conv2 = self.block2_conv1(input2)
        conv2 = self.block2_conv2(conv2)
        pool2 = self.block2_pool1(conv2)

        input3 = self.block3_input1(scale_img_2)
        input3 = tf.concat([input3, pool2], axis=3)
        conv3 = self.block3_conv1(input3)
        conv3 = self.block3_conv2(conv3)
        pool3 = self.block3_pool1(conv3)

        input4 = self.block4_input1(scale_img_3)
        input4 = tf.concat([input4, pool3], axis=3)
        conv4 = self.block4_conv1(input4)
        conv4 = self.block4_conv2(conv4)
        pool4 = self.block4_pool1(conv4)

        conv5 = self.block5_conv1(pool4)
        conv5 = self.block5_conv2(conv5)

        temp6 = self.block6_dconv(conv5)
        up6 = tf.concat([temp6, conv4], axis=3)
        conv6 = self.block6_conv1(up6)
        conv6 = self.block6_conv2(conv6)

        temp7 = self.block7_dconv(conv6)
        up7 = tf.concat([temp7, conv3], axis=3)
        conv7 = self.block7_conv1(up7)
        conv7 = self.block7_conv2(conv7)

        temp8 = self.block8_dconv(conv7)
        up8 = tf.concat([temp8, conv2], axis=3)
        conv8 = self.block8_conv1(up8)
        conv8 = self.block8_conv2(conv8)

        temp9 = self.block9_dconv(conv8)
        up9 = tf.concat([temp9, conv1], axis=3)
        conv9 = self.block9_conv1(up9)
        conv9 = self.block9_conv2(conv9)

        side6 = UpSampling2D(size=(8, 8))(conv6)
        side7 = UpSampling2D(size=(4, 4))(conv7)
        side8 = UpSampling2D(size=(2, 2))(conv8)

        out6 = self.side63(side6)
        out7 = self.side73(side7)
        out8 = self.side83(side8)
        out9 = self.side93(conv9)

        out10 = average([out6, out7, out8, out9])

        return [out6, out7, out8, out9, out10]

#u-net model function api
def DeepModel(size_set=640):

    img_input = Input(shape=(size_set, size_set, 3))

    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    conv1 = Conv2D(32, (3, 3), activation='relu', padding='same', name='block1_conv2')(conv1)
    pool1 = MaxPool2D(pool_size=(2, 2))(conv1)

    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block2_conv1')(pool1)
    conv2 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block2_conv2')(conv2)
    pool2 = MaxPool2D(pool_size=(2, 2))(conv2)

    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block3_conv1')(pool2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block3_conv2')(conv3)
    pool3 = MaxPool2D(pool_size=(2, 2))(conv3)

    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block4_conv1')(pool3)
    conv4 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block4_conv2')(conv4)
    pool4 = MaxPool2D(pool_size=(2, 2))(conv4)

    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(pool4)
    conv5 = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(conv5)

    up6 = concatenate(
        [Conv2DTranspose(256, (2, 2), strides=(2, 2), padding='same', name='block6_dconv')(conv5), conv4],
        axis=3)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block6_conv1')(up6)
    conv6 = Conv2D(256, (3, 3), activation='relu', padding='same', name='block6_conv2')(conv6)

    up7 = concatenate(
        [Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same', name='block7_dconv')(conv6), conv3],
        axis=3)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block7_conv1')(up7)
    conv7 = Conv2D(128, (3, 3), activation='relu', padding='same', name='block7_conv2')(conv7)

    up8 = concatenate([Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same', name='block8_dconv')(conv7), conv2],
                      axis=3)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block8_conv1')(up8)
    conv8 = Conv2D(64, (3, 3), activation='relu', padding='same', name='block8_conv2')(conv8)

    up9 = concatenate([Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same', name='block9_dconv')(conv8), conv1],
                      axis=3)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same', name='block9_conv1')(up9)
    conv9 = Conv2D(32, (3, 3), activation='relu', padding='same', name='block9_conv2')(conv9)

    side6 = UpSampling2D(size=(8, 8))(conv6)
    side7 = UpSampling2D(size=(4, 4))(conv7)
    side8 = UpSampling2D(size=(2, 2))(conv8)
    out6 = Conv2D(1, (1, 1), activation='sigmoid', name='side_6')(side6)
    out7 = Conv2D(1, (1, 1), activation='sigmoid', name='side_7')(side7)
    out8 = Conv2D(1, (1, 1), activation='sigmoid', name='side_8')(side8)
    out9 = Conv2D(1, (1, 1), activation='sigmoid', name='side_9')(conv9)

    out10 = average([out6, out7, out8, out9])
    return Model(inputs=img_input, outputs=out10)