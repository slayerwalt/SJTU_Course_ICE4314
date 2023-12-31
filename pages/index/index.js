Page({
    data: {
        image: '',
        message: '',
        message_receive:'',
    },

    chooseImage: function () {
        var that = this;
        wx.chooseImage({
            count: 1,
            success: function (res) {
                var tempFilePath = res.tempFilePaths[0];
                that.setData({
                    image: tempFilePath,
                });
            }
        });
    },

    viewImage: function () {
        var image = this.data.image;
        if (image) {
            wx.previewImage({
                urls: [image]
            });
        } else {
            wx.showToast({
                title: '请先上传图片',
                icon: 'none',
                duration: 2000
            });
        }
    },

    inputChange: function (e) {
        this.setData({
            message: e.detail.value
        });
    },

    // encryptMessage: function (message) {
    //     let encryptedMessage = '';
    //     for (let i = 0; i < message.length; i++) {
    //         encryptedMessage += String.fromCharCode(message.charCodeAt(i) ^ 0xF0);
    //     }
    //     return encryptedMessage;
    //     //return message;
    // },

    sendMessage: function () {
        let message = this.data.message;
        // let encryptedMessage = this.encryptMessage(message);

        // 发送加密后的消息和图片
        wx.uploadFile({
            url: 'http://59.78.57.189:11451/',
            // url:'http://192.168.31.80:8000',
            filePath: this.data.image,
            name: 'image',
            formData: {
                message: message,
            },
            success: (res) => {
                console.log("上传完成")
                console.log(res.data)
            },
            fail: (err) => {
                console.log("上传失败", err); // 输出上传失败的错误信息
            }
        })
    },

    getMessage: function () {
        var that = this;
        wx.request({
            url: 'http://59.78.57.189:11451/get',
            // url: 'http://192.168.31.80:8000/get',
            method: 'GET',
            responseType: 'text',
            success: function (res) {
                if (res.statusCode === 200) {
                    that.setData({
                        message_receive: res.data
                    });
                    console.log('接受成功');
                } else {
                    console.error('获取消息失败');
                }
            },
            fail: function (error) {
                console.error('请求失败' + error);
            },
        })
    },
});