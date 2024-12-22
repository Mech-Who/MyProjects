<template>
  <div class="PeopleInfo">
    <h4>PeopleInfo: {{ currentId }}</h4>
    <el-form
      ref="form"
      :disabled="formDisable"
      :model="peopleInfo"
      label-width="80px"
    >
      <el-form-item label="姓名" prop="name">
        <el-input
          placeholder="请填写姓名"
          :maxLength="20"
          v-model="peopleInfo.name"
        ></el-input>
      </el-form-item>
      <el-form-item label="性别" prop="gender">
        <el-select
          placeholder="请选择性别"
          v-model="peopleInfo.gender"
        ></el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from "vue-router";
import { onMounted, reactive, watch } from "vue";
import fsRequest from "@/service";

/********** 路由传参初始化 **********/
const route = useRoute();
let currentId = route.params.peopleId;
let formDisable = true;
watch(
  () => route.params.id,
  (newId, oldId) => {
    // 对路由变化做出响应...
    console.log(`newId: ${newId}, oldId: ${oldId}`);
    currentId = newId;
  }
);

/********** 获取人员信息并展示 **********/
interface PeopleInfo {
  name: string;
  birthday: string;
  gender: number;
  favor: number;
  latestEvent: Event[];
}
let peopleInfo = reactive<PeopleInfo>({
  name: "",
  birthday: "",
  gender: 0,
  favor: 0.0,
  latestEvent: [],
});

interface IResponseData {
  name: string;
  birthday: string;
  gender: number;
  favor: number;
  latest_event: Event[];
}

const getPeopleInfo = () => {
  fsRequest
    .request<IResponseData>({
      url: "/people/get_info",
      method: "post",
      data: {
        id: currentId,
      },
    })
    .then((res) => {
      let data = res.data;
      peopleInfo.name = data.name;
      peopleInfo.birthday = data.birthday;
      peopleInfo.gender = data.gender;
      peopleInfo.favor = data.favor;
      peopleInfo.latestEvent = data.latest_event;
    })
    .catch((err) => {
      console.log(err);
    });
};

/********** 生命周期 **********/
onMounted(() => {
  getPeopleInfo();
});
</script>

<style scoped></style>
