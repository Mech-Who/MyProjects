<template>
  <div class="PeopleInfo">
    <h4>PeopleInfo: {{ currentId }}</h4>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { watch } from "vue";

const route = useRoute();
let currentId = route.params.peopleId;
watch(
  () => route.params.id,
  (newId, oldId) => {
    // 对路由变化做出响应...
    console.log(`newId: ${newId}, oldId: ${oldId}`);
    currentId = newId;
  }
);
</script>

<style scoped></style>
