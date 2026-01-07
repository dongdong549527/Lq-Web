<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

interface Granary {
  id: number
  name: string
  depot_id: number
  collection_status: number
  info?: {
    design_capacity: number
    actual_capacity: number
    manager: string
    storage_nature: string
    variety: string
    entry_time: string
    origin: string
    grade: string
    rough_rice_yield: number
    moisture: number
    remark: string
  }
  config?: {
    extension_number: number
    temp_collector_count: number
    th_collector_count: number
    start_index: number
    end_index: number
    th_index: number
    cable_count: number
    cable_point_count: number
    total_collector_count: number
    mqtt_topic_sub: string
    mqtt_topic_pub: string
    collection_device: number
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
const activeTab = ref('basic')

const form = reactive({
  id: 0,
  name: '',
  depot_id: undefined as number | undefined,
  info: {
    design_capacity: 0,
    actual_capacity: 0,
    manager: '',
    storage_nature: '',
    variety: '',
    entry_time: '',
    origin: '',
    grade: '',
    rough_rice_yield: 0,
    moisture: 0,
    remark: ''
  },
  config: {
    extension_number: 0,
    temp_collector_count: 0,
    th_collector_count: 0,
    start_index: 0,
    end_index: 0,
    th_index: 0,
    cable_count: 0,
    cable_point_count: 0,
    total_collector_count: 0,
    mqtt_topic_sub: '',
    mqtt_topic_pub: '',
    collection_device: 0
  }
})

const rules = {
  name: [{ required: true, message: '请输入粮仓名称', trigger: 'blur' }],
  depot_id: [{ required: true, message: '请选择所属粮库', trigger: 'change' }]
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
  form.depot_id = undefined
  // Reset nested objects
  form.info = {
    design_capacity: 0,
    actual_capacity: 0,
    manager: '',
    storage_nature: '',
    variety: '',
    entry_time: null as unknown as string,
    origin: '',
    grade: '',
    rough_rice_yield: 0,
    moisture: 0,
    remark: ''
  }
  form.config = {
    extension_number: 0,
    temp_collector_count: 0,
    th_collector_count: 0,
    start_index: 0,
    end_index: 0,
    th_index: 0,
    cable_count: 0,
    cable_point_count: 0,
    total_collector_count: 0,
    mqtt_topic_sub: '',
    mqtt_topic_pub: '',
    collection_device: 0
  }
  activeTab.value = 'basic'
  dialogVisible.value = true
}

const handleEdit = (row: Granary) => {
  isEdit.value = true
  activeTab.value = 'basic'
  form.id = row.id
  form.name = row.name
  form.depot_id = row.depot_id
  
  // Fill nested objects or reset if missing
  if (row.info) {
    Object.assign(form.info, row.info)
  } else {
    Object.assign(form.info, {
      design_capacity: 0,
      actual_capacity: 0,
      manager: '',
      storage_nature: '',
      variety: '',
      entry_time: '',
      origin: '',
      grade: '',
      rough_rice_yield: 0,
      moisture: 0,
      remark: ''
    })
  }
  
  if (row.config) {
    Object.assign(form.config, row.config)
  } else {
    Object.assign(form.config, {
        extension_number: 0,
        temp_collector_count: 0,
        th_collector_count: 0,
        start_index: 0,
        end_index: 0,
        th_index: 0,
        cable_count: 0,
        cable_point_count: 0,
        total_collector_count: 0,
        mqtt_topic_sub: '',
        mqtt_topic_pub: '',
        collection_device: 0
    })
  }
  
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
        if (isEdit.value) {
            await request.put(`/granaries/${form.id}`, form)
            ElMessage.success('更新成功')
        } else {
            await request.post('/granaries', form)
            ElMessage.success('创建成功')
        }
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
      <el-table-column label="设计容量 (吨)" align="right">
          <template #default="scope">
              {{ scope.row.info?.design_capacity || '-' }}
          </template>
      </el-table-column>
      <el-table-column label="实际储量 (吨)" align="right">
          <template #default="scope">
              {{ scope.row.info?.actual_capacity || '-' }}
          </template>
      </el-table-column>
      <el-table-column label="仓管员" align="center">
          <template #default="scope">
              {{ scope.row.info?.manager || '-' }}
          </template>
      </el-table-column>
      <el-table-column label="采集状态" align="center">
          <template #default="scope">
               <el-tag :type="scope.row.collection_status === 1 ? 'success' : 'info'">
                  {{ scope.row.collection_status === 1 ? '采集中' : '空闲' }}
               </el-tag>
          </template>
      </el-table-column>
      <el-table-column label="操作" width="180" align="center">
        <template #default="scope">
          <el-button size="small" type="primary" plain @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="danger" plain @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑粮仓' : '新增粮仓'"
      width="60%"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px" status-icon>
        <el-tabs v-model="activeTab">
            <!-- 基础信息 -->
            <el-tab-pane label="基本信息" name="basic">
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
                        <el-form-item label="设计容量 (吨)">
                          <el-input-number v-model="form.info.design_capacity" :min="0" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="实际储量 (吨)">
                          <el-input-number v-model="form.info.actual_capacity" :min="0" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="仓管员">
                     <el-input v-model="form.info.manager" placeholder="请输入仓管员姓名" />
                </el-form-item>
            </el-tab-pane>

            <!-- 粮情信息 -->
            <el-tab-pane label="粮情信息" name="info">
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="存储性质">
                           <el-input v-model="form.info.storage_nature" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="品种">
                           <el-input v-model="form.info.variety" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="产地">
                           <el-input v-model="form.info.origin" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="等级">
                           <el-input v-model="form.info.grade" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row :gutter="20">
                    <el-col :span="12">
                        <el-form-item label="出糙率">
                           <el-input-number v-model="form.info.rough_rice_yield" :precision="2" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="水分 (%)">
                           <el-input-number v-model="form.info.moisture" :precision="2" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-form-item label="入仓时间">
                    <el-date-picker v-model="form.info.entry_time" type="datetime" placeholder="选择入仓时间" style="width: 100%" />
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="form.info.remark" type="textarea" />
                </el-form-item>
            </el-tab-pane>

            <!-- 硬件配置 -->
            <el-tab-pane label="硬件配置" name="config">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-form-item label="分机号">
                            <el-input-number v-model="form.config.extension_number" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="采集设备ID">
                            <el-input-number v-model="form.config.collection_device" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="8">
                        <el-form-item label="采集器总数">
                            <el-input-number v-model="form.config.total_collector_count" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-row>
                
                <el-divider content-position="left">电缆配置</el-divider>
                <el-row :gutter="20">
                     <el-col :span="12">
                        <el-form-item label="电缆根数">
                            <el-input-number v-model="form.config.cable_count" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="单根点数">
                            <el-input-number v-model="form.config.cable_point_count" style="width: 100%" />
                        </el-form-item>
                    </el-col>
                </el-row>

                <el-divider content-position="left">MQTT 配置</el-divider>
                <el-form-item label="订阅主题">
                    <el-input v-model="form.config.mqtt_topic_sub" />
                </el-form-item>
                <el-form-item label="发布主题">
                    <el-input v-model="form.config.mqtt_topic_pub" />
                </el-form-item>
            </el-tab-pane>
        </el-tabs>
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
