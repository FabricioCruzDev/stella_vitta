<script setup>
import { useRouter } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <header class="main-header">
      <div class="header-content">
        <div class="logo" @click="$router.push('/')">
          <span class="brand-stella">Stella</span><span class="brand-vita">-Vita</span>
        </div>
        <nav class="main-nav">
          <router-link to="/" class="nav-link">Dashboard</router-link>
          <router-link to="/novo-usuario" class="nav-link">Membros</router-link>
        </nav>
      </div>
    </header>

    <main class="page-content">
      <router-view />
    </main>
  </div>
</template>

<style>
/* Reset e Estilos Globais */
:root {
  --primary: #4f46e5;
  --bg-body: #f9fafb;
  --text-main: #111827;
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background-color: var(--bg-body);
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  padding: 1.25rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  width: 95%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  cursor: pointer;
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.brand-stella { color: var(--primary); }
.brand-vita { color: var(--text-main); }

.nav-link {
  margin-left: 2rem;
  text-decoration: none;
  color: #6b7280;
  font-weight: 600;
  font-size: 0.95rem;
  transition: color 0.2s;
}

.nav-link:hover { color: var(--primary); }
.nav-link.router-link-active {
  color: var(--primary);
  border-bottom: 2px solid var(--primary);
  padding-bottom: 4px;
}

.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>