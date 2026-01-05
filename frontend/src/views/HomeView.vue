<script setup lang="ts">
import { ref } from 'vue'

// 使用 Element Plus 的卡片和图标来美化首页
const features = ref([
  {
    title: '粮库管理',
    description: '管理所有粮库的基本信息和地理位置',
    icon: 'OfficeBuilding',
    route: '/depots',
    color: '#409EFF'
  },
  {
    title: '粮仓管理',
    description: '监控粮仓库存、容量及温湿度环境',
    icon: 'Box',
    route: '/granaries',
    color: '#67C23A'
  },
  {
    title: '用户管理',
    description: '系统用户权限与账号管理',
    icon: 'User',
    route: '/users',
    color: '#E6A23C'
  }
])
</script>

<template>
  <div class="home-container">
    <div class="welcome-section">
      <h1 class="main-title">欢迎使用智慧粮仓管理系统</h1>
      <p class="subtitle">Smart Grain Depot Management System</p>
    </div>

    <el-row :gutter="20" class="features-row">
      <el-col :span="8" v-for="item in features" :key="item.title">
        <router-link :to="item.route" class="feature-link">
          <el-card shadow="hover" class="feature-card">
            <div class="card-content">
              <el-icon :size="48" :color="item.color">
                <component :is="item.icon" />
              </el-icon>
              <h3>{{ item.title }}</h3>
              <p>{{ item.description }}</p>
            </div>
          </el-card>
        </router-link>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.home-container {
  padding: 40px;
  text-align: center;
}

.welcome-section {
  margin-bottom: 60px;
}

.main-title {
  font-size: 2.5rem;
  color: #303133;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 1.2rem;
  color: #909399;
  letter-spacing: 2px;
}

.features-row {
  max-width: 1200px;
  margin: 0 auto;
}

.feature-link {
  text-decoration: none;
}

.feature-card {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.card-content h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #303133;
}

.card-content p {
  margin: 0;
  font-size: 0.9rem;
  color: #606266;
}
</style>
