<template>
  <div class="ManageLayout">
    <el-container>
      <el-aside width="200px">
        <el-menu :default-active="current" mode="vertical" router>
          <el-menu-item index="/people">人员管理</el-menu-item>
          <el-menu-item index="/event">事件管理</el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { ref } from "vue";

let current = ref("/index");
</script>

<style scoped></style>
