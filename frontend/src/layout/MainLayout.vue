<script setup lang="ts">
import { RouterView, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = () => {
    authStore.logout()
    router.push('/login')
}
</script>

<template>
  <el-container class="layout-container">
    <el-header>
      <div class="header-inner">
        <div class="logo">
             <el-icon class="logo-icon" :size="24"><Platform /></el-icon>
             <span>智慧粮仓管理系统</span>
        </div>
        <el-menu
          mode="horizontal"
          :ellipsis="false"
          router
          class="header-menu"
          :default-active="$route.path"
        >
          <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>首页
          </el-menu-item>
          <el-menu-item index="/depots">
              <el-icon><OfficeBuilding /></el-icon>粮库管理
          </el-menu-item>
          <el-menu-item index="/granaries">
              <el-icon><Box /></el-icon>粮仓管理
          </el-menu-item>
          <el-menu-item index="/users">
              <el-icon><User /></el-icon>用户管理
          </el-menu-item>
        </el-menu>
        <div class="user-actions">
            <el-dropdown>
                <span class="el-dropdown-link">
                  管理员 <el-icon class="el-icon--right"><arrow-down /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
            </el-dropdown>
        </div>
      </div>
    </el-header>
    
    <el-main>
      <div class="main-content">
        <RouterView />
      </div>
    </el-main>
  </el-container>
</template>

<style scoped>
.layout-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 2px 8px #f0f1f2;
  z-index: 10;
  padding: 0;
  height: 60px;
}

.header-inner {
    max-width: 1400px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 20px;
}

.logo {
    display: flex;
    align-items: center;
    font-size: 20px;
    font-weight: bold;
    color: #303133;
    margin-right: 60px;
    white-space: nowrap;
}

.logo-icon {
    margin-right: 10px;
    color: var(--el-color-primary);
}

.header-menu {
    flex: 1;
    border-bottom: none !important;
    height: 100%;
}

.el-menu-item {
    font-size: 15px;
    height: 60px;
    line-height: 60px;
}

.el-main {
    padding: 24px;
    overflow-y: auto;
}

.main-content {
    max-width: 1400px;
    margin: 0 auto;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #606266;
}

.el-dropdown-link:hover {
    color: var(--el-color-primary);
}
</style>
