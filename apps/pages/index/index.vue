<template>
	<uni-notice-bar scrollable single text="苹果医生是基于飞桨和Fastdelopy的苹果叶面病害识别程序,致力于为植物病虫害识别提供落地解决方案."></uni-notice-bar>

	<view>
		<image src="/static/1.jpg" class="banner"></image>
	</view>
	<view class="step">
		<uni-steps :options="process" :active="stepActive"></uni-steps>
	</view>
	<view>
		<image src="/static/icon/photo.png" class="uploadImg" @click="selectImg" v-if="result.disease === '等待上传'"></image>
		<image :src="result.imageUrl" v-else class="showImg" @click="selectImg"></image>
		<button :type="result['status']" @click="selectImg" class="resultBtn" plain=true>{{ result['disease'] }}</button>
	</view>
	
</template>

<script>
	import uniSteps from '/uni_modules/uni-steps/components/uni-steps/uni-steps.vue';
	import uniNoticeBar from '/uni_modules/uni-notice-bar/components/uni-notice-bar/uni-notice-bar.vue';
	
	export default {
		components:{
			uniSteps,
			uniNoticeBar
		},
		data() {
			return {
				process: [
					{title: '拍摄图片'},
					{title: '图片上传'},
					{title: '模型推理'},
					{title: '诊断结果'}
				],
				result: {
					"status": "default",
					"disease": "等待上传",
					"imageUrl": "",
				},
				stepActive: 0,
			}
		},
		onLoad() {

		},
		methods: {
			selectImg(){
				let that = this;
				uni.chooseImage({
					count: 1,
					success: function (res) {
						console.log(res)
						console.log(JSON.stringify(res.tempFilePaths));
						that.result.imageUrl = res.tempFilePaths[0];
						that.stepActive = 2;
						uni.uploadFile({
							url: 'http://xjh.free.svipss.top/image/', //仅为示例，非真实的接口地址
							filePath: res.tempFilePaths[0],
							name: 'file',
							success: (uploadFileRes) => {
								console.log(uploadFileRes.data);
								let data = JSON.parse(uploadFileRes.data);
								that.result.status = data.status
								that.result.disease = data.disease
								that.stepActive = 3;
							},
							})
					}
				})
			}
		}
	}
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}
	.banner{
		display: block;
		width: 100%;
		height: 120px;
		margin: 0 auto;
	}
	.step{
		margin-top: 20px;
	}
	
	.resultBtn{
		margin-top: 30px;
		width: 50%;
		display: block;
		
	}
	
	.uploadImg{
		display: block;
		width: 200px;
		height: 170px;
		margin: 0 auto;
		margin-top: 50px;
	}
	
	.showImg{
		display: block;
		margin: 0 auto;
		margin-top: 50px;
	}
</style>
