<template>
  <div class="calendar">
    <div class="header">
      <button @click="prevMonth">‹</button>
      <span>{{ currentYear }} 年 {{ currentMonth + 1 }} 月</span>
      <button @click="nextMonth">›</button>
    </div>
    <div class="weekdays">
      <span v-for="day in weekDays" :key="day">{{ day }}</span>
    </div>
    <div class="days">
      <span 
        v-for="day in calendarDays" 
        :key="day.date" 
        :class="{
          'disabled': !day.isClickable,
          'today': day.isToday,
          'clickable': day.isClickable
        }"
        @click="updateDate(day)"
      >
        {{ day.day }}
      </span>
    </div>
    <!-- 回到当前月份按钮 -->
    <button @click="resetToCurrentMonth" class="reset-button">回到当前月份</button>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import dayjs from "dayjs";

const emit = defineEmits('updateDate');

// 传入的时间参数列表
const props = defineProps({
  dateList: Array // ["2025-03-04 01:50:49", "2025-03-10 12:00:00"]
});

// 获取所有可点击的日期（去除时分秒）
const clickableDates = computed(() => {
  return new Set(props.dateList.map(date => dayjs(date).format("YYYY-MM-DD")));
});

// 当前月份和年份
const currentYear = ref(dayjs().year());
const currentMonth = ref(dayjs().month());

const weekDays = ["日", "一", "二", "三", "四", "五", "六"];

// 计算当前月份的日期数组
const calendarDays = computed(() => {
  const firstDayOfMonth = dayjs().year(currentYear.value).month(currentMonth.value).date(1);
  const lastDayOfMonth = firstDayOfMonth.endOf("month");

  const prevMonthDays = firstDayOfMonth.day(); // 前面需要补的空格数
  const totalDays = lastDayOfMonth.date();

  const days = [];

  // 上个月的填充
  for (let i = prevMonthDays - 1; i >= 0; i--) {
    days.push({ day: "", date: "", isClickable: false });
  }

  // 当前月份的日期
  for (let i = 1; i <= totalDays; i++) {
    const dateStr = dayjs().year(currentYear.value).month(currentMonth.value).date(i).format("YYYY-MM-DD");
    days.push({
      day: i,
      date: dateStr,
      isClickable: clickableDates.value.has(dateStr),
      isToday: dateStr === dayjs().format("YYYY-MM-DD")
    });
  }

  return days;
});

// 切换月份
const prevMonth = () => {
  if (currentMonth.value === 0) {
    currentYear.value--;
    currentMonth.value = 11;
  } else {
    currentMonth.value--;
  }
};

const nextMonth = () => {
  if (currentMonth.value === 11) {
    currentYear.value++;
    currentMonth.value = 0;
  } else {
    currentMonth.value++;
  }
};

// 处理点击
const updateDate = (day) => {
  if (day.isClickable) {
    emit('updateDate', day.date);
  }
};

// 回到当前月份
const resetToCurrentMonth = () => {
  currentYear.value = dayjs().year();
  currentMonth.value = dayjs().month();
};
</script>

<style scoped>
.calendar {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  background: rgba(255, 255, 255, 0.8);
  padding: 16px;
  text-align: center;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

.header button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.weekdays {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  font-weight: bold;
  margin-bottom: 5px;
}

.days {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
}

.days span {
  width: 25px;
  height: 25px;
  line-height: 25px;
  border-radius: 50%;
  text-align: center;
  cursor: pointer;
}

.disabled {
  color: #ccc;
  pointer-events: none;
}

.clickable {
  background-color: lightblue;
}

.today {
  background-color: lightcoral;
  color: white;
  font-weight: bold;
}

.reset-button {
  margin-top: 20px;
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
  background-color: #0c0e0c36;
  color: white;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.reset-button:hover {
  background-color: #457da0;
}
</style>
