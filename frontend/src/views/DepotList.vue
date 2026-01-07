<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

interface Depot {
  id: number
  name: string
  address: string
  contact_person: string
  phone: string
  province: string
  created_at: string
}

const depots = ref<Depot[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = reactive({
  id: 0,
  name: '',
  address: '',
  contact_person: '',
  phone: '',
  province: ''
})

const rules = {
  name: [{ required: true, message: '请输入粮库名称', trigger: 'blur' }]
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
  form.address = ''
  form.contact_person = ''
  form.phone = ''
  form.province = ''
  dialogVisible.value = true
}

const handleEdit = (row: Depot) => {
  isEdit.value = true
  form.id = row.id
  form.name = row.name
  form.address = row.address
  form.contact_person = row.contact_person
  form.phone = row.phone
  form.province = row.province
  dialogVisible.value = true
}

const handleDelete = (row: Depot) => {
  ElMessageBox.confirm('确定要删除该粮库吗?', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await request.delete(`/depots/${row.id}`)
      ElMessage.success('删除成功')
      fetchDepots()
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
          await request.put(`/depots/${form.id}`, form)
          ElMessage.success('更新成功')
        } else {
          await request.post('/depots', form)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchDepots()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

onMounted(() => {
  fetchDepots()
})
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span class="title">粮库管理</span>
        <el-button type="primary" @click="handleAdd">
            <el-icon class="el-icon--left"><Plus /></el-icon>
            新增粮库
        </el-button>
      </div>
    </template>

    <el-table :data="depots" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" align="center" />
      <el-table-column prop="name" label="粮库名称" />
      <el-table-column prop="province" label="省份" width="100" />
      <el-table-column prop="address" label="粮库地址" show-overflow-tooltip />
      <el-table-column prop="contact_person" label="联系人" width="120" />
      <el-table-column prop="phone" label="电话" width="150" />
      <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
              {{ new Date(scope.row.created_at).toLocaleString() }}
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
      :title="isEdit ? '编辑粮库' : '新增粮库'"
      width="40%"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" status-icon>
        <el-form-item label="粮库名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入粮库名称" />
        </el-form-item>
        <el-form-item label="省份" prop="province">
          <el-input v-model="form.province" placeholder="请输入省份" />
        </el-form-item>
        <el-form-item label="粮库地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址" />
        </el-form-item>
        <el-row :gutter="20">
            <el-col :span="12">
                <el-form-item label="联系人" prop="contact_person">
                  <el-input v-model="form.contact_person" placeholder="请输入联系人" />
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="电话" prop="phone">
                  <el-input v-model="form.phone" placeholder="请输入联系电话" />
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
