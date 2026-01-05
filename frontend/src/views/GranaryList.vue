<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

interface Granary {
  id: number
  name: string
  capacity: number
  current_stock: number
  depot_id: number
  config?: {
    temperature_threshold_high: number
    humidity_threshold_high: number
  }
}

interface Depot {
  id: number
  name: string
}

const granaries = ref<Granary[]>([])
const depots = ref<Depot[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = reactive({
  id: 0,
  name: '',
  capacity: 0,
  current_stock: 0,
  depot_id: undefined as number | undefined,
  config: {
    temperature_threshold_high: 30,
    humidity_threshold_high: 60
  }
})

const rules = {
  name: [{ required: true, message: '请输入粮仓名称', trigger: 'blur' }],
  depot_id: [{ required: true, message: '请选择所属粮库', trigger: 'change' }],
  capacity: [{ required: true, message: '请输入容量', trigger: 'blur' }]
}

const fetchGranaries = async () => {
  try {
    const res = await request.get('/granaries')
    granaries.value = res as unknown as Granary[]
  } catch (error) {
    ElMessage.error('获取粮仓列表失败')
  }
}

const fetchDepots = async () => {
  try {
    const res = await request.get('/depots')
    depots.value = res as unknown as Depot[]
  } catch (error) {
    ElMessage.error('获取粮库列表失败')
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.id = 0
  form.name = ''
  form.capacity = 1000
  form.current_stock = 0
  form.depot_id = undefined
  form.config = { temperature_threshold_high: 30, humidity_threshold_high: 60 }
  dialogVisible.value = true
}

const handleDelete = (row: Granary) => {
  ElMessageBox.confirm('确定要删除该粮仓吗?', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await request.delete(`/granaries/${row.id}`)
      ElMessage.success('删除成功')
      fetchGranaries()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const submitForm = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      try {
        await request.post('/granaries', form)
        ElMessage.success('创建成功')
        dialogVisible.value = false
        fetchGranaries()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

const getDepotName = (id: number) => {
    const depot = depots.value.find(d => d.id === id)
    return depot ? depot.name : '未知粮库'
}

onMounted(() => {
  fetchGranaries()
  fetchDepots()
})
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span class="title">粮仓管理</span>
        <el-button type="primary" @click="handleAdd">
             <el-icon class="el-icon--left"><Plus /></el-icon>
            新增粮仓
        </el-button>
      </div>
    </template>

    <el-table :data="granaries" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" align="center" />
      <el-table-column prop="name" label="粮仓名称" />
      <el-table-column label="所属粮库">
          <template #default="scope">
              {{ getDepotName(scope.row.depot_id) }}
          </template>
      </el-table-column>
      <el-table-column prop="capacity" label="容量 (吨)" align="right" />
      <el-table-column prop="current_stock" label="当前库存 (吨)" align="right" />
      <el-table-column label="环境阈值 (温/湿)" width="180" align="center">
        <template #default="scope">
          <el-tag type="warning" size="small">{{ scope.row.config?.temperature_threshold_high }}°C</el-tag>
          <span style="margin: 0 5px">/</span>
          <el-tag type="info" size="small">{{ scope.row.config?.humidity_threshold_high }}%</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120" align="center">
        <template #default="scope">
          <el-button size="small" type="danger" plain @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      title="新增粮仓"
      width="40%"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" status-icon>
        <el-form-item label="粮仓名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入粮仓名称" />
        </el-form-item>
        <el-form-item label="所属粮库" prop="depot_id">
          <el-select v-model="form.depot_id" placeholder="请选择粮库" style="width: 100%">
            <el-option
              v-for="item in depots"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-row :gutter="20">
            <el-col :span="12">
                <el-form-item label="设计容量 (吨)" prop="capacity">
                  <el-input-number v-model="form.capacity" :min="0" style="width: 100%" />
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="初始库存 (吨)" prop="current_stock">
                  <el-input-number v-model="form.current_stock" :min="0" style="width: 100%" />
                </el-form-item>
            </el-col>
        </el-row>
        
        <el-divider content-position="left">环境预警配置</el-divider>
        
        <el-row :gutter="20">
            <el-col :span="12">
                <el-form-item label="高温预警 (°C)">
                  <el-input-number v-model="form.config.temperature_threshold_high" style="width: 100%" />
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="高湿预警 (%)">
                  <el-input-number v-model="form.config.humidity_threshold_high" :min="0" :max="100" style="width: 100%" />
                </el-form-item>
            </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitForm">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
</template>

<style scoped>
.box-card {
    margin: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title {
    font-size: 18px;
    font-weight: bold;
    color: var(--el-text-color-primary);
}
</style>
