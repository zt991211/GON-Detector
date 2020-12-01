//index.js
//获取应用实例
const app = getApp()
const ip = app.ip
Page({
    data: {
        motto: '还没有数据',
        userInfo: {},
        hasUserInfo: false,
        canIUse: wx.canIUse('button.open-type.getUserInfo'),
        id: null,
        img: null,
        imgPath: null,
        level:  null
    },
    //事件处理函数
    bindViewTap: function() {
        wx.navigateTo({
            url: '../logs/logs'
        })
    },
    onLoad: function() {
        if (app.globalData.userInfo) {
            this.setData({
                userInfo: app.globalData.userInfo,
                hasUserInfo: true
            })
        } else if (this.data.canIUse) {
            // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
            // 所以此处加入 callback 以防止这种情况
            app.userInfoReadyCallback = res => {
                this.setData({
                    userInfo: res.userInfo,
                    hasUserInfo: true
                })
            }
        } else {
            // 在没有 open-type=getUserInfo 版本的兼容处理
            wx.getUserInfo({
                success: res => {
                    app.globalData.userInfo = res.userInfo
                    this.setData({
                        userInfo: res.userInfo,
                        hasUserInfo: true
                    })
                }
            })
        }
    },

    getUserInfo: function(e) {
        console.log(e)
        app.globalData.userInfo = e.detail.userInfo
        this.setData({
            userInfo: e.detail.userInfo,
            hasUserInfo: true
        })
    },

    chooseImage1: function () {
        var that = this;

        wx.chooseImage({
            count: 1,
            sizeType: ['original', 'compressed'],
            sourceType: ['album', 'camera'],
            success(res) {
                // tempFilePatxh可以作为img标签的src属性显示图片
                const tempFilePaths = res.tempFilePaths[0]
                console.log(tempFilePaths[0])
                that.setData({
                    userHeaderImage: tempFilePaths,
                    imgPath: tempFilePaths
                })
                console.log(tempFilePaths)
                //上传图片
                wx.showLoading({
                    title: '上传图片中...',
                })
                wx.uploadFile({
                    url: ip + '/uploader',
                    filePath: tempFilePaths,
                    name: 'photo', //后台要绑定的名称
                    // header: {
                    //   "content-type": "multipart/form-data",
                    //   'content-type': 'application/x-www-form-urlencoded' //表单提交
                    // },
                    header: { "content-type": "multipart/form-data"},
                    formData: {
                        'id': that.data.id  //参数绑定
                    },
                    success(res) {
                        const data = res.data
                        console.log(res);
                        console.log('**************')
                        console.log('upload_img:' + res.data)
                        console.log('**************')
                        that.setData({
                            img: true,
                            id:  res.data
                        })
                        console.log('tttttttttt')
                        console.log(that.data.id)
                        //do something
                    },
                    complete() {
                        wx.hideLoading()
                    }
                })
            }, 
            fail(err) {
                console.log("img上传失败：" + err.errMsg)
            }
        })
    },
    

    getresult: function() {
        var that = this

        wx.showLoading({
            title: '获取处理结果',
        })
        console.log('获取处理结果')
        wx.request({
            url: ip+'/vx/' + that.data.id,
            data: {

            },
            header: {
                'content-type': 'application/json' // 默认值
            },
            success(res) {
                console.log(res.data)
                //console.log(type(res.data))
                if (res.data == "-2") {
                    wx.showToast({
                        title: '数据未处理完',
                        icon: 'none',
                        duration: 5000
                    })
                    return
                }
                that.setData({
                    level: res.data
                })
                wx.showToast({
                    title: '数据获取成功',
                    icon: 'success',
                    duration: 5000
                })
            },
            fail(err) {
                wx.showToast({
                    title: '获取失败！',
                    icon: 'none',
                    duration: 3000
                })
                console.log('获取失败！')
            },
            complete() {
                wx.hideLoading()
            }
        })
    },
    
    diagnose: function() {
        var that = this
        wx.showLoading({
            title: '后台算法处理',
        })
        console.log('后台算法开始处理')
        console.log(that.data.id)
        console.log(ip + '/vx/' + that.data.id)
        wx.request({
            url: ip+'/vx/'+that.data.id,
            data: {
                
            },
            header: {
                'content-type': 'application/json' // 默认值
            },
            success(res) {
                console.log(res.data)
                if (res.data == "-1") {
                    wx.showToast({
                        title: '数据处理过程出错，可过一段时间重试',
                        duration: 5000
                    })
                    that.setData({
                        level: '数据处理过程出错，可过一段时间重试'
                    })
                    return
                }
                that.setData({
                    level: res.data
                })
                wx.showToast({
                    title: '数据获取成功',
                    icon: 'success',
                    duration: 5000
                })
            },
            fail(err) {
                wx.showToast({
                    title: '获取失败！',
                    icon: 'none',
                    duration: 3000
                })
                console.log('诊断失败！')
            },
            complete() {
                wx.hideLoading()
            }
        })
    }
})