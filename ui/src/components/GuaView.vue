<template>
  <a-card title="易经占卜">
    <!-- 起卦步骤 -->
    <template v-if="!hexagramData">
      <a-form :model="formState" @finish="onCastHexagram" layout="vertical">
        <a-form-item label="性别" name="gender">
          <a-select v-model:value="formState.gender" placeholder="请选择性别">
            <a-select-option value="boy">男</a-select-option>
            <a-select-option value="girl">女</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="需求" name="demand">
          <a-select
            v-model:value="formState.demand"
            placeholder="请选择您的需求"
          >
            <a-select-option value="事业">事业</a-select-option>
            <a-select-option value="爱情">爱情</a-select-option>
            <a-select-option value="健康">健康</a-select-option>
            <a-select-option value="财运">财运</a-select-option>
            <a-select-option value="学业">学业</a-select-option>
            <a-select-option value="其他">其他</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item>
          <a-alert
            message="起卦说明"
            description="点击 '起卦' 按钮时，系统将根据当前精确的时间节点（年月日时分秒）进行64卦换算，确保每一卦的唯一性和时效性。"
            type="info"
            show-icon
            style="margin-bottom: 16px;"
          />
          <a-button type="primary" html-type="submit" :loading="casting">
            起卦
          </a-button>
        </a-form-item>
      </a-form>
    </template>

    <!-- 卦象显示和分析步骤 -->
    <template v-if="hexagramData">
      <a-divider />
      <h3>卦象结果</h3>
      <div style="text-align: left; margin-bottom: 20px;">
        <p><strong>本卦：</strong>{{ hexagramData.bengua.gua }}</p>
        <p><strong>下卦：</strong>{{ hexagramData.bengua.xiagua }}</p>
        <p><strong>上卦：</strong>{{ hexagramData.bengua.shanggua }}</p>
        <p><strong>动爻：</strong>{{ hexagramData.bengua.dongyao.join(', ') || '无' }}</p>
        <p><strong>变卦：</strong>{{ hexagramData.biangua.gua }}</p>
      </div>

      <a-form :model="formState" @finish="onAnalyzeHexagram" layout="vertical">
        <a-form-item label="性别" name="gender">
          <a-select v-model:value="formState.gender" placeholder="请选择性别">
            <a-select-option value="boy">男</a-select-option>
            <a-select-option value="girl">女</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="需求" name="demand">
          <a-select
            v-model:value="formState.demand"
            placeholder="请选择您的需求"
          >
            <a-select-option value="事业">事业</a-select-option>
            <a-select-option value="爱情">爱情</a-select-option>
            <a-select-option value="健康">健康</a-select-option>
            <a-select-option value="财运">财运</a-select-option>
            <a-select-option value="学业">学业</a-select-option>
            <a-select-option value="其他">其他</a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item>
          <a-button type="primary" html-type="submit" :loading="analyzing">
            开始分析
          </a-button>
          <a-button style="margin-left: 10px" @click="resetHexagram">
            重新起卦
          </a-button>
        </a-form-item>
      </a-form>

      <template v-if="resultData">
        <a-divider />
        <h3>分析结果</h3>
        <div style="text-align: left;">
          <div v-html="markdownResult"></div>
        </div>
      </template>
    </template>
  </a-card>
</template>

<script>
import { defineComponent, reactive, ref, computed } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import { marked } from 'marked'; // 引入 marked
import { API_BASE_URL } from '../api/config';

export default defineComponent({
  name: 'GuaView',
  setup() {
    const formState = reactive({
      gender: '',
      demand: '',
    });

    const hexagramData = ref(null);
    const resultData = ref(null);
    const casting = ref(false);
    const analyzing = ref(false);

    const markdownResult = computed(() => {
      if (resultData.value) {
        const md = `
### 卦象：${resultData.value.gua}

### 动爻：${resultData.value.dongyao}

### 变卦：${resultData.value.biangua}

### 解读：
${resultData.value.result}
`;
        return marked(md); // 使用 marked 解析 Markdown
      }
      return '';
    });

    const onCastHexagram = async (values) => {
      casting.value = true;
      try {
        const response = await axios.post(`${API_BASE_URL}/zhanbu/cast_hexagram`, {}, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        });

        if (response.data.status === 'success') {
          hexagramData.value = response.data.hexagram_data;
          resultData.value = null; // 清空之前的分析结果
          message.success('起卦成功！');
        } else if (response.data.status === 'limited') {
          message.warning(response.data.message);
        } else {
          message.error('起卦失败，请稍后再试。');
        }
      } catch (error) {
        console.error('起卦请求出错:', error);
        message.error('起卦请求出错，请检查网络连接。');
      } finally {
        casting.value = false;
      }
    };

    const onAnalyzeHexagram = async (values) => {
      if (!hexagramData.value) {
        message.error('请先起卦！');
        return;
      }

      analyzing.value = true;
      try {
        const payload = {
          gender: values.gender,
          demand: values.demand,
          hexagram_data: hexagramData.value
        };

        const response = await axios.post(`${API_BASE_URL}/zhanbu/analyze_hexagram`, payload, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
        });

        if (response.data.status === 'success') {
          resultData.value = response.data;
          message.success('分析完成！');
        } else if (response.data.status === 'limited') {
          message.warning(response.data.message);
        } else {
          message.error('分析失败，请稍后再试。');
        }
      } catch (error) {
        console.error('分析请求出错:', error);
        message.error('分析请求出错，请检查网络连接。');
      } finally {
        analyzing.value = false;
      }
    };

    const resetHexagram = () => {
      hexagramData.value = null;
      resultData.value = null;
    };

    return {
      formState,
      hexagramData,
      resultData,
      casting,
      analyzing,
      onCastHexagram,
      onAnalyzeHexagram,
      resetHexagram,
      markdownResult,
    };
  },
});
</script>

<style scoped>
/* 可以添加一些样式调整，例如卡片宽度等 */
/* 移除 pre 和 code 的样式，交给 marked 处理 */
</style>
