import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useUserStore } from '@/stores/user'
// 按需导入 Vant 组件
import {
  Tabbar,
  TabbarItem,
  Icon,
  Search,
  Button,
  Popup,
  Field,
  RadioGroup,
  Radio,
  Uploader,
  Form,
  Toast,
  PullRefresh,
  List,
  DropdownMenu,
  DropdownItem,
  ActionSheet,
  NavBar,
  Empty,
  Loading,
  ImagePreview,
  showToast,
  closeToast,
} from 'vant'

import 'vant/lib/index.css'

// 导入 Leaflet 样式
import 'leaflet/dist/leaflet.css'

const app = createApp(App)

// 注册 Vant 组件
app.use(Tabbar)
app.use(TabbarItem)
app.use(Icon)
app.use(Search)
app.use(Button)
app.use(Popup)
app.use(Field)
app.use(RadioGroup)
app.use(Radio)
app.use(Uploader)
app.use(Form)
app.use(Toast)
app.use(PullRefresh)
app.use(List)
app.use(DropdownMenu)
app.use(DropdownItem)
app.use(ActionSheet)
app.use(NavBar)
app.use(Empty)
app.use(Loading)
app.use(ImagePreview)
app.use(showToast, closeToast)

app.use(createPinia())
app.use(router)

const userStore = useUserStore()
userStore.init()

app.mount('#app')
