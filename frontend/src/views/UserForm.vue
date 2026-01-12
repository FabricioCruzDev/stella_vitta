<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const isSaving = ref(false)

// Estado inicial do formulário
const newUser = ref({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
  role: 'retail',
  user_type_id: 3 // Varejo por padrão
})

// Mapeamento automático (Backend precisa desses IDs)
const roleToIdMap = {
  'admin': 1,
  'wholesale': 2,
  'retail': 3
}

// Observa a mudança na Role e atualiza o ID silenciosamente
watch(() => newUser.value.role, (newRole) => {
  newUser.value.user_type_id = roleToIdMap[newRole]
})

const addUser = async () => {
  isSaving.value = true
  try {
    await axios.post('http://localhost:8000/users/', newUser.value)
    alert("Usuário cadastrado com sucesso!")
    router.push('/') // Volta para o dashboard
  } catch (error) {
    console.error(error)
    alert("Erro ao salvar: " + (error.response?.data?.detail || "Erro no servidor"))
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div class="page-wrapper">
    <div class="form-card">
      <div class="form-header">
        <h2>Novo Membro</h2>
        <p>Preencha os dados para criar um novo acesso.</p>
      </div>

      <form @submit.prevent="addUser">
        <div class="form-row">
          <div class="form-group">
            <label>Nome</label>
            <input v-model="newUser.first_name" type="text" placeholder="Ex: João" required />
          </div>
          <div class="form-group">
            <label>Sobrenome</label>
            <input v-model="newUser.last_name" type="text" placeholder="Ex: Silva" required />
          </div>
        </div>

        <div class="form-group">
          <label>E-mail</label>
          <input v-model="newUser.email" type="email" placeholder="email@stellavita.com" required />
        </div>

        <div class="form-group">
          <label>Senha Provisória</label>
          <input v-model="newUser.password" type="password" placeholder="••••••••" required />
        </div>

        <div class="form-group">
          <label>Nível de Acesso (Role)</label>
          <select v-model="newUser.role">
            <option value="admin">Administrador</option>
            <option value="wholesale">Atacado</option>
            <option value="retail">Varejo</option>
          </select>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-cancel" @click="router.push('/')">
            Cancelar
          </button>
          <button type="submit" class="btn-save" :disabled="isSaving">
            {{ isSaving ? 'Salvando...' : 'Cadastrar Membro' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Container principal que ocupa o espaço abaixo do header e centraliza o card */
.page-wrapper {
  display: flex;
  align-items: center;     /* Centraliza Verticalmente */
  justify-content: center;  /* Centraliza Horizontalmente */
  min-height: 80vh;        /* Garante altura suficiente para o centro */
  padding: 2rem;
  width: 100%;
  box-sizing: border-box;
}

.form-card {
  background: #ffffff;
  width: 100%;
  max-width: 500px;        /* Largura fixa do formulário */
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  border: 1px solid #e5e7eb;
}

.form-header {
  margin-bottom: 2rem;
  text-align: center;
}

.form-header h2 {
  margin: 0;
  color: #111827;
  font-size: 1.75rem;
}

.form-header p {
  color: #6b7280;
  margin-top: 0.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
  text-align: left;
}

input, select {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
}

input:focus, select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-save {
  flex: 2;
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-save:hover {
  background-color: #4338ca;
}

.btn-save:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.btn-cancel {
  flex: 1;
  background-color: transparent;
  color: #6b7280;
  border: 1px solid #d1d5db;
  padding: 0.8rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.btn-cancel:hover {
  background-color: #f9fafb;
  color: #111827;
}

/* Ajuste para telas pequenas */
@media (max-width: 480px) {
  .form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>