<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const users = ref([])
const isLoading = ref(true)

const loadUsers = async () => {
  isLoading.value = true
  try {
    const response = await axios.get('http://localhost:8000/users/')
    users.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    isLoading.value = false
  }
}

const deleteUser = async (id) => {
  if (confirm("Deseja excluir este membro?")) {
    try {
      await axios.delete(`http://localhost:8000/users/${id}`)
      loadUsers()
    } catch (error) {
      alert("Erro ao excluir")
    }
  }
}

onMounted(loadUsers)
</script>

<template>
  <div class="dashboard-wrapper">
    <div class="dashboard-header">
      <div class="title-section">
        <h2>Gestão de Usuários</h2>
        <p>Controle de acessos e permissões Stella Vita</p>
      </div>
      
      <router-link to="/novo-usuario" class="btn-primary-add">
        <span class="plus-icon">+</span> Novo Usuário
      </router-link>
    </div>

    <div class="table-container">
      <table v-if="!isLoading">
        <thead>
          <tr>
            <th>Nome Completo</th>
            <th>E-mail</th>
            <th>Permissão</th>
            <th class="actions-col">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="user-name">{{ user.first_name }} {{ user.last_name }}</td>
            <td>{{ user.email }}</td>
            <td><span class="role-badge">{{ user.role }}</span></td>
            <td class="actions-col">
              <button @click="deleteUser(user.id)" class="btn-delete-table">Excluir</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="loader">Carregando usuários...</div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-wrapper {
  padding: 3rem 2.5%; /* Largura total com respiro lateral */
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 2.5rem;
}

.title-section h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #111827;
}

.title-section p {
  margin: 0.5rem 0 0 0;
  color: #6b7280;
}

/* BOTÃO IGUAL AO DO FORMULÁRIO */
.btn-primary-add {
  background-color: #4f46e5;
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  transition: all 0.2s;
  box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2);
}

.btn-primary-add:hover {
  background-color: #4338ca;
  transform: translateY(-1px);
}

.plus-icon { font-size: 1.3rem; line-height: 1; }

/* TABELA ESTILIZADA */
.table-container {
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  background-color: #f9fafb;
  padding: 1.25rem;
  text-align: left;
  font-size: 0.85rem;
  text-transform: uppercase;
  color: #4b5563;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 1.25rem;
  border-bottom: 1px solid #f3f4f6;
  color: #374151;
}

.user-name { font-weight: 600; color: #111827; }

.role-badge {
  background: #eef2ff;
  color: #4f46e5;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: capitalize;
}

.actions-col { text-align: right; }

.btn-delete-table {
  background: none;
  border: 1px solid #fee2e2;
  color: #ef4444;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.btn-delete-table:hover {
  background-color: #ef4444;
  color: white;
}

.loader { padding: 4rem; text-align: center; color: #6b7280; }
</style>