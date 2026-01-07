<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import request from '@/api/request'
import { ElMessage, ElMessageBox } from 'element-plus'

interface User {
  id: number
  username: string
  email: string
  full_name: string
  phone: string
  role: number
  depot_id: number | null
  is_active: boolean
}

interface Depot {
  id: number
  name: string
}

const users = ref<User[]>([])
const depots = ref<Depot[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref()

const form = reactive({
  id: 0,
  username: '',
  email: '',
  password: '',
  full_name: '',
  phone: '',
  role: 0,
  depot_id: undefined as number | undefined,
  is_active: true
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur', type: 'email' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const fetchUsers = async () => {
  try {
    const res = await request.get('/users')
    users.value = res as unknown as User[]
  } catch (error) {
    ElMessage.error('获取用户列表失败')
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
  form.username = ''
  form.email = ''
  form.password = ''
  form.full_name = ''
  form.phone = ''
  form.role = 0
  form.depot_id = undefined
  form.is_active = true
  dialogVisible.value = true
}

const handleEdit = (row: User) => {
  isEdit.value = true
  form.id = row.id
  form.username = row.username
  form.email = row.email
  form.password = '' // Don't show password
  form.full_name = row.full_name
  form.phone = row.phone
  form.role = row.role
  form.depot_id = row.depot_id || undefined
  form.is_active = row.is_active
  dialogVisible.value = true
}

const handleDelete = (row: User) => {
  ElMessageBox.confirm('确定要删除该用户吗?', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(async () => {
    try {
      await request.delete(`/users/${row.id}`)
      ElMessage.success('删除成功')
      fetchUsers()
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
        // 如果是编辑且密码为空，则不提交密码字段（后端逻辑需要支持，或者前端过滤）
        // 这里简单处理：如果密码为空且是编辑模式，后端应该忽略密码更新（已在后端实现）
        const data = { ...form }
        if (isEdit.value && !data.password) {
            delete (data as any).password
        }
        
        if (isEdit.value) {
          await request.put(`/users/${form.id}`, data)
          ElMessage.success('更新成功')
        } else {
          await request.post('/users', data)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        fetchUsers()
      } catch (error) {
        ElMessage.error('操作失败')
      }
    }
  })
}

const getDepotName = (id: number | null) => {
    if (!id) return '-'
    const depot = depots.value.find(d => d.id === id)
    return depot ? depot.name : '未知粮库'
}

onMounted(() => {
  fetchUsers()
  fetchDepots()
})
</script>

<template>
  <el-card class="box-card">
    <template #header>
      <div class="card-header">
        <span class="title">用户管理</span>
        <el-button type="primary" @click="handleAdd">
            <el-icon class="el-icon--left"><Plus /></el-icon>
            新增用户
        </el-button>
      </div>
    </template>

    <el-table :data="users" stripe style="width: 100%">
      <el-table-column prop="id" label="ID" width="80" align="center" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="full_name" label="姓名" />
      <el-table-column prop="role" label="角色" align="center">
          <template #default="scope">
              <el-tag :type="scope.row.role === 1 ? 'danger' : 'success'">
                  {{ scope.row.role === 1 ? '管理员' : '普通用户' }}
              </el-tag>
          </template>
      </el-table-column>
      <el-table-column label="所属粮库">
          <template #default="scope">
              {{ getDepotName(scope.row.depot_id) }}
          </template>
      </el-table-column>
      <el-table-column prop="phone" label="电话" />
      <el-table-column prop="email" label="邮箱" show-overflow-tooltip />
      <el-table-column prop="is_active" label="状态" align="center" width="80">
          <template #default="scope">
              <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                  {{ scope.row.is_active ? '启用' : '禁用' }}
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
      :title="isEdit ? '编辑用户' : '新增用户'"
      width="40%"
      destroy-on-close
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" status-icon>
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="form.full_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-row :gutter="20">
            <el-col :span="12">
                <el-form-item label="角色" prop="role">
                  <el-select v-model="form.role" placeholder="请选择角色" style="width: 100%">
                    <el-option label="普通用户" :value="0" />
                    <el-option label="管理员" :value="1" />
                  </el-select>
                </el-form-item>
            </el-col>
            <el-col :span="12">
                <el-form-item label="所属粮库" prop="depot_id">
                  <el-select v-model="form.depot_id" placeholder="请选择粮库" style="width: 100%" clearable>
                    <el-option
                      v-for="item in depots"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                    />
                  </el-select>
                </el-form-item>
            </el-col>
        </el-row>
        <el-form-item label="状态" prop="is_active">
             <el-switch v-model="form.is_active" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        
        <el-divider />
        
        <el-form-item label="密码" prop="password" v-if="!isEdit">
           <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="password" v-if="isEdit">
           <el-input v-model="form.password" type="password" placeholder="留空则不修改" show-password />
        </el-form-item>
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
