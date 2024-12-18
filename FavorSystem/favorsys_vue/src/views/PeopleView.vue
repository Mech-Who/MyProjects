<template>
  <div class="people">
    <h1>人员列表</h1>
    <el-table :data="peopleData" border>
      <el-table-column type="expand">
        <template #default="props">
          <div>
            近期事件:
            {{ props.row.latestEvent ? props.row.latestEvent.length : 0 }}
          </div>
          <el-table
            v-if="props.row.latestEvent"
            :data="props.row.latestEvent"
            border
            width="auto"
          >
            <el-table-column label="序号" prop="id" width="100" />
            <el-table-column label="标题" prop="title" width="100" />
            <el-table-column label="描述" prop="description" width="100" />
            <el-table-column
              label="好感度影响"
              prop="favorEffect"
              width="100"
            />
          </el-table>
        </template>
      </el-table-column>
      <el-table-column label="序号" prop="id" width="100" />
      <el-table-column label="姓名">
        <template #default="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓别">
        <template #default="scope">
          <span>{{ scope.row.gender == 1 ? "男" : "女" }}</span>
        </template>
      </el-table-column>
      <el-table-column label="生日">
        <template #default="scope">
          <span>{{ scope.row.birthday }}</span>
        </template>
      </el-table-column>
      <el-table-column label="好感值" width="1000">
        <template #default="scope">
          <el-progress
            :percentage="scope.row.favor"
            :format="favorFormat"
            :color="favorColors"
          />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="145" fixed="right">
        <template #default="scope">
          <el-button-group>
            <el-button type="primary" @click="modifyPeopleInfo(scope.row)"
              >编辑</el-button
            >
            <el-button type="danger" @click="deletePeopleInfo(scope.row)"
              >删除</el-button
            >
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { People } from "../entities/entity";

const router = useRouter();

const modifyPeopleInfo = (row: People) => {
  console.log(row);
  router.push(`/people/${row.id}`);
};
const deletePeopleInfo = (row: object) => {
  console.log(row);
};

const favorColors = [
  { color: "#f56c6c", percentage: 100 },
  { color: "#e6a23c", percentage: 80 },
  { color: "#5cb87a", percentage: 60 },
  { color: "#1989fa", percentage: 40 },
  { color: "#6f7ad3", percentage: 20 },
];

const favorLevel = [
  "厌恶至极", // 0
  "心生不满", // 10
  "形同陌路", // 20
  "一面之缘", // 30
  "点头之交", // 40
  "泛泛之交", // 50
  "心生好感", // 60
  "值得相交", // 70
  "情深义重", // 80
  "终生伴侣", // 90
  "至死不渝", // 100
];

const favorFormat = (percentage: number) => {
  if (percentage < 0 || percentage > 100) return "错误";
  for (let level = 10; level >= 0; --level) {
    if (percentage >= level * 10) return `${favorLevel[level]}(${percentage}%)`;
  }
};

const peopleData = [
  {
    id: 1,
    name: "胡舒涵",
    birthday: "2001-08-20",
    gender: 1,
    favor: 100.0,
    latestEvent: [
      {
        id: 1,
        title: "Event 1",
        description: "Description 1",
        favorEffect: +10,
      },
      {
        id: 2,
        title: "Event 2",
        description: "Description 2",
        favorEffect: -10,
      },
    ],
  },
  {
    id: 2,
    name: "张三",
    birthday: "2000-04-22",
    gender: 0,
    favor: 90.5,
    // latestEvent: [],
  },
  {
    id: 3,
    name: "李四",
    birthday: "2002-03-10",
    gender: 0,
    favor: 80.5,
    latestEvent: [],
  },
  {
    id: 4,
    name: "王五",
    birthday: "2003-11-10",
    gender: 0,
    favor: 70.5,
    latestEvent: [],
  },
  {
    id: 5,
    name: "赵六",
    birthday: "1999-05-21",
    gender: 0,
    favor: 60.5,
    latestEvent: [],
  },
  {
    id: 6,
    name: "李华",
    birthday: "2001-05-20",
    gender: 1,
    favor: 50.5,
    latestEvent: [],
  },
  {
    id: 7,
    name: "赵空城",
    birthday: "1987-06-23",
    gender: 1,
    favor: 40.5,
    latestEvent: [],
  },
  {
    id: 8,
    name: "李泽铭",
    birthday: "1997-01-05",
    gender: 1,
    favor: 30.5,
    latestEvent: [],
  },
  {
    id: 9,
    name: "赵雪",
    birthday: "2005-08-08",
    gender: 0,
    favor: 20.5,
    latestEvent: [],
  },
  {
    id: 10,
    name: "李斯武",
    birthday: "2003-05-05",
    gender: 1,
    favor: 10.5,
    latestEvent: [],
  },
  {
    id: 11,
    name: "刘琳琳",
    birthday: "1999-12-25",
    gender: 0,
    favor: 0.5,
    latestEvent: [],
  },
];
</script>

<style scoped></style>
