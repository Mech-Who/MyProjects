<template>
  <el-container>
    <el-header>
      <el-menu mode="horizontal" router>
        <el-menu-item index="/home">首页</el-menu-item>
        <el-menu-item index="/about">关于</el-menu-item>
        <el-sub-menu index="/manage">
          <template #title>系统管理</template>
          <el-menu-item index="/people">人员管理</el-menu-item>
          <el-menu-item index="/event">事件管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script lang="ts" setup></script>

<style lang="less">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
