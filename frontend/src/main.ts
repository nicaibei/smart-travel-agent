/**
 * 主应用入口
 */
import { createApp } from 'vue';
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import App from './App.vue';
import router from './router';

// 创建应用实例
const app = createApp(App);

// 使用Ant Design Vue
app.use(Antd);

// 使用路由
app.use(router);

// 挂载应用
app.mount('#app');
