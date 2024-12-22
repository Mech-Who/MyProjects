<template>
  <div class="people">
    <el-row :gutter="0">
      <el-col :span="24">
        <el-text size="large" tag="b">人员列表</el-text>
      </el-col>
    </el-row>
    <el-row :gutter="0">
      <el-col :span="1">
        <el-button type="primary" @click="dialogVisible = true">添加</el-button>
      </el-col>
    </el-row>
    <el-table :data="peopleData" border max-height="600">
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
      <el-table-column fixed label="序号" prop="id" width="80" />
      <el-table-column fixed label="姓名" width="100">
        <template #default="scope">
          <span>{{ scope.row.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="姓别" width="60">
        <template #default="scope">
          <span>{{ scope.row.gender == 1 ? "男" : "女" }}</span>
        </template>
      </el-table-column>
      <el-table-column label="生日" width="100">
        <template #default="scope">
          <span>{{ scope.row.birthday }}</span>
        </template>
      </el-table-column>
      <el-table-column label="好感值" style="width: 100%">
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
            <el-button type="primary" @click="goPeopleInfo(scope.row.id)"
              >详情</el-button
            >
            <el-popconfirm
              title="你确定要删除吗?"
              confirm-button-text="确认"
              cancel-button-text="取消"
              @confirm="deletePeopleInfo(scope.row)"
              @cancel="cancelDelete"
            >
              <template #reference>
                <el-button type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      background
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="totalCount"
      :pager-count="pagerCount"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="TableSizeChange"
      @current-change="TablePageChange"
    />
    <!-- 弹出框，用来添加人员 -->
    <el-dialog
      v-model="dialogVisible"
      title="人员添加"
      width="30%"
      :before-close="beforeDialogClose"
    >
      <el-form
        ref="peopleCreateFormRef"
        :model="peopleCreateForm"
        :rules="peopleCreateRules"
      >
        <el-form-item label="姓名" required>
          <el-input
            v-model="peopleCreateForm.name"
            placeholder="请输入姓名"
            clearable
          />
        </el-form-item>
        <el-form-item label="性别" required>
          <el-radio-group v-model="peopleCreateForm.gender">
            <el-radio label="1">男</el-radio>
            <el-radio label="0">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="出生日期" required>
          <el-date-picker
            v-model="peopleCreateForm.birthday"
            type="date"
            placeholder="选择日期"
            value-format="YYYY-MM-DD"
            clearable
          />
        </el-form-item>
        <el-form-item label="好感度" required>
          <el-slider
            v-model.number="peopleCreateForm.favor"
            :min="minFavor"
            :max="maxFavor"
            show-input
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="createPeople"> 添加 </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, computed, ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { People } from "../entities/entity";
import { ElMessage } from "element-plus";
import type { FormInstance, FormRules } from "element-plus";
import fsRequest from "@/service";

const router = useRouter();

/********** 好感度展示 **********/
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

/********** 添加人员 **********/
let minFavor = ref(0);
let maxFavor = ref(100);
let dialogVisible = ref(false);
interface PeopleCreateForm {
  name: string;
  birthday: string;
  gender: number;
  favor: number;
}
let peopleCreateForm = reactive<PeopleCreateForm>({
  name: "",
  birthday: "",
  gender: 0,
  favor: 0.0,
});

const peopleCreateRules = reactive<FormRules<PeopleCreateForm>>({
  name: [
    {
      required: true,
      message: "请输入姓名",
      trigger: "change",
    },
  ],
  birthday: [
    {
      required: true,
      message: "请选择出生日期",
      trigger: "change",
    },
  ],
  gender: [
    {
      required: true,
      message: "请选择性别",
      trigger: "change",
    },
  ],
});
const beforeDialogClose = () => {
  peopleCreateForm.name = "";
  peopleCreateForm.birthday = "";
  peopleCreateForm.gender = 0;
  peopleCreateForm.favor = 0.0;
};

const createPeople = () => {
  // console.log("创建人员！");
  // console.log(peopleCreateForm.birthday);
  fsRequest
    .request<IResponseData>({
      url: "/people/create",
      method: "post",
      data: [peopleCreateForm],
    })
    .then((res) => {
      console.log(res);
      // 成功提示
      ElMessage({
        message: `[${peopleCreateForm.name}]添加成功!`,
        type: "success",
      });
    });

  // 关闭弹窗
  dialogVisible.value = false;
};

/********** 人员列表 **********/
let pagerCount = ref(5);
let totalCount = ref(0);
let pageSize = ref(20);
let totalPage = ref(0);
let realPage = ref(0);
let currentPage = computed({
  get: () => {
    return realPage.value + 1;
  },
  set: (newPage) => {
    realPage.value = newPage - 1;
  },
});
let peopleData = ref([
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
]);

interface IResponseData {
  args: any;
  headers: any;
  origin: string;
  url: string;
  people_list: [];
  total_page: number;
  current_page: number;
  total_count: number;
}

const getPeopleList = (page_size: number, page_num: number) => {
  /**
   * page_total: 一页有多少项
   * page_num: 第几页，从0开始
   */
  fsRequest
    .request<IResponseData>({
      url: "/people/list",
      method: "post",
      data: {
        page_size: page_size,
        page_num: page_num,
      },
    })
    .then((res) => {
      let data = res.data;
      console.log(data);
      peopleData.value = data.people_list;
      totalPage.value = data.total_page;
      totalCount.value = data.total_count;
    });
};

const goPeopleInfo = (people_id: number) => {
  console.log(people_id);
  router.push(`/people/${people_id}`);
};

const deletePeopleInfo = (people: People) => {
  /**
   * 根据 people_id 删除人员。
   * people_id: 要删除的人员的id。
   */
  console.log(people);
  fsRequest
    .request<IResponseData>({
      url: "/people/delete",
      method: "post",
      data: [{ id: people.id }],
    })
    .then((res) => {
      console.log(res);
      peopleData.value = peopleData.value.filter((p) => p.id != people.id);
      ElMessage({
        message: `[${people.name}]删除成功!`,
        type: "success",
      });
    });
};

const cancelDelete = () => {
  console.log("取消操作！");
};

const TableSizeChange = (newSize: number) => {
  pageSize.value = newSize;
  getPeopleList(pageSize.value, realPage.value);
};

const TablePageChange = (newPage: number) => {
  currentPage.value = newPage;
  getPeopleList(pageSize.value, realPage.value);
};

/********** 生命周期 **********/
onMounted(() => {
  // console.log("onMounted");
  getPeopleList(20, 0);
});
</script>

<style scoped></style>
