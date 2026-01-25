<template>
  <div class="gua-container">
    <!-- 标题卡片 -->
    <div class="title-card">
      <div class="title-icon">☷</div>
      <h1 class="page-title">易经占卜</h1>
      <p class="page-subtitle">诚心问卦，AI 为你解读天机</p>
    </div>

    <!-- 起卦表单 -->
    <transition name="fade-slide" mode="out-in">
      <div v-if="!hexagramData" class="form-card">
        <div class="form-header">
          <h3>请输入占卜信息</h3>
        </div>
        
        <a-form :model="formState" @finish="onCastHexagram" layout="vertical">
          <a-form-item label="性别" name="gender">
            <a-radio-group v-model:value="formState.gender" size="large">
              <a-radio-button value="boy">男</a-radio-button>
              <a-radio-button value="girl">女</a-radio-button>
            </a-radio-group>
          </a-form-item>

          <a-form-item label="占卜事项" name="demand">
            <a-select
              v-model:value="formState.demand"
              placeholder="请选择您的占卜事项"
              size="large"
            >
              <a-select-option value="事业">事业</a-select-option>
              <a-select-option value="爱情">爱情</a-select-option>
              <a-select-option value="健康">健康</a-select-option>
              <a-select-option value="财运">财运</a-select-option>
              <a-select-option value="学业">学业</a-select-option>
              <a-select-option value="其他">其他</a-select-option>
            </a-select>
          </a-form-item>

          <a-alert
            message="起卦说明"
            description="点击「起卦」按钮时，系统将根据当前精确的时间节点（年月日时分秒）进行64卦换算，确保每一卦的唯一性和时效性。"
            type="info"
            show-icon
            class="info-alert"
          />

          <a-form-item>
            <a-button 
              type="primary" 
              html-type="submit" 
              :loading="casting"
              size="large"
              block
              class="submit-btn"
            >
              <template v-if="!casting">🎲 开始起卦</template>
              <template v-else>起卦中...</template>
            </a-button>
          </a-form-item>
        </a-form>
      </div>

      <!-- 卦象显示 -->
      <div v-else class="hexagram-display">
        <!-- 卦象结果卡片 -->
        <div class="hexagram-card">
          <div class="hexagram-header">
            <h3>卦象结果</h3>
          </div>
          
          <div class="hexagram-grid">
            <div class="hexagram-item">
              <div class="hexagram-label">本卦</div>
              <div class="hexagram-value main-gua">{{ hexagramData.bengua.gua }}</div>
            </div>
            <div class="hexagram-item">
              <div class="hexagram-label">变卦</div>
              <div class="hexagram-value change-gua">{{ hexagramData.biangua.gua }}</div>
            </div>
            <div class="hexagram-item">
              <div class="hexagram-label">下卦</div>
              <div class="hexagram-value">{{ hexagramData.bengua.xiagua }}</div>
            </div>
            <div class="hexagram-item">
              <div class="hexagram-label">上卦</div>
              <div class="hexagram-value">{{ hexagramData.bengua.shanggua }}</div>
            </div>
            <div class="hexagram-item full-width">
              <div class="hexagram-label">动爻</div>
              <div class="hexagram-value">
                <span v-if="hexagramData.bengua.dongyao.length > 0">
                  {{ hexagramData.bengua.dongyao.join(', ') }}
                </span>
                <span v-else class="no-value">无</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 分析表单 -->
        <div class="analysis-form-card">
          <div class="form-header">
            <h3>开始分析</h3>
          </div>
          
          <a-form :model="formState" @finish="onAnalyzeHexagram" layout="vertical">
            <a-form-item label="性别" name="gender">
              <a-radio-group v-model:value="formState.gender" size="large">
                <a-radio-button value="boy">男</a-radio-button>
                <a-radio-button value="girl">女</a-radio-button>
              </a-radio-group>
            </a-form-item>

            <a-form-item label="占卜事项" name="demand">
              <a-select
                v-model:value="formState.demand"
                placeholder="请选择您的占卜事项"
                size="large"
              >
                <a-select-option value="事业">事业</a-select-option>
                <a-select-option value="爱情">爱情</a-select-option>
                <a-select-option value="健康">健康</a-select-option>
                <a-select-option value="财运">财运</a-select-option>
                <a-select-option value="学业">学业</a-select-option>
                <a-select-option value="其他">其他</a-select-option>
              </a-select>
            </a-form-item>

            <div class="button-group">
              <a-button 
                type="primary" 
                html-type="submit" 
                :loading="analyzing"
                size="large"
                class="analyze-btn"
              >
                <template v-if="!analyzing">AI 智能分析</template>
                <template v-else>分析中...</template>
              </a-button>
              <a-button 
                size="large" 
                @click="resetHexagram"
                class="reset-btn"
              >
                重新起卦
              </a-button>
            </div>
          </a-form>
        </div>
      </div>
    </transition>

    <!-- 分析结果 -->
    <transition name="fade-slide">
      <div v-if="resultData" class="result-section">
        <div class="result-header">
          <h2 class="result-title">卦象解读</h2>
        </div>
        <div class="result-content">
          <div class="markdown-body" v-html="markdownResult"></div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { defineComponent, reactive, ref, computed } from 'vue';
import { message } from 'ant-design-vue';
import axios from 'axios';
import { marked } from 'marked';
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
        return marked(md);
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
          resultData.value = null;
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
.gua-container {
  width: 100%;
  animation: fadeIn 0.6s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ========== Title Card ========== */
.title-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  text-align: center;
  margin-bottom: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.title-icon {
  font-size: 64px;
  margin-bottom: 16px;
  animation: pulse 3s ease-in-out infinite;
  color: #764ba2;
  display: inline-block;
  position: relative;
}

.title-icon::before {
  content: '☰☱☲☳☴☵☶☷';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 12px;
  color: rgba(102, 126, 234, 0.2);
  letter-spacing: 2px;
  animation: rotate 30s linear infinite reverse;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.9; }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 16px;
  color: #666;
}

/* ========== Form Card ========== */
.form-card,
.analysis-form-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.form-header {
  margin-bottom: 24px;
}

.form-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.form-card :deep(.ant-form-item-label > label),
.analysis-form-card :deep(.ant-form-item-label > label) {
  font-weight: 600;
  font-size: 15px;
  color: #333;
}

.form-card :deep(.ant-radio-button-wrapper),
.analysis-form-card :deep(.ant-radio-button-wrapper) {
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  margin-right: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.form-card :deep(.ant-radio-button-wrapper:hover),
.analysis-form-card :deep(.ant-radio-button-wrapper:hover) {
  border-color: #667eea;
}

.form-card :deep(.ant-radio-button-wrapper-checked),
.analysis-form-card :deep(.ant-radio-button-wrapper-checked) {
  border-color: #667eea !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.form-card :deep(.ant-select-selector),
.analysis-form-card :deep(.ant-select-selector) {
  border-radius: 12px;
  border: 2px solid #e0e0e0;
  height: 50px;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.form-card :deep(.ant-select-selector:hover),
.analysis-form-card :deep(.ant-select-selector:hover),
.form-card :deep(.ant-select-focused .ant-select-selector),
.analysis-form-card :deep(.ant-select-focused .ant-select-selector) {
  border-color: #667eea;
}

.info-alert {
  margin-bottom: 24px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.info-alert :deep(.ant-alert-message) {
  font-weight: 600;
  color: #667eea;
}

.submit-btn {
  height: 50px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

/* ========== Hexagram Display ========== */
.hexagram-display {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.hexagram-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.hexagram-header {
  margin-bottom: 24px;
}

.hexagram-header h3 {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hexagram-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.hexagram-item {
  background: rgba(102, 126, 234, 0.05);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.hexagram-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.hexagram-item:hover::before {
  transform: scaleX(1);
}

.hexagram-item:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-3px);
}

.hexagram-item.full-width {
  grid-column: 1 / -1;
}

.hexagram-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 12px;
  font-weight: 500;
}

.hexagram-value {
  font-size: 18px;
  color: #333;
  font-weight: 600;
}

.hexagram-value.main-gua {
  font-size: 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hexagram-value.change-gua {
  font-size: 24px;
  color: #764ba2;
}

.no-value {
  color: #ccc;
  font-size: 16px;
}

/* ========== Button Group ========== */
.button-group {
  display: flex;
  gap: 12px;
}

.analyze-btn {
  flex: 2;
  height: 50px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.analyze-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.reset-btn {
  flex: 1;
  height: 50px;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  border: 2px solid #e0e0e0;
  background: white;
  color: #666;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  border-color: #667eea;
  color: #667eea;
  transform: translateY(-2px);
}

/* ========== Result Section ========== */
.result-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.result-header {
  text-align: center;
  margin-bottom: 32px;
}

.result-title {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.result-content {
  background: rgba(102, 126, 234, 0.03);
  border-radius: 12px;
  padding: 30px;
}

.markdown-body {
  font-size: 15px;
  line-height: 1.8;
  color: #333;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  color: #667eea;
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 700;
}

.markdown-body :deep(h3) {
  font-size: 20px;
  padding-bottom: 8px;
  border-bottom: 2px solid rgba(102, 126, 234, 0.2);
}

.markdown-body :deep(p) {
  margin-bottom: 16px;
  line-height: 1.8;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 24px;
  margin-bottom: 16px;
}

.markdown-body :deep(li) {
  margin-bottom: 8px;
}

.markdown-body :deep(strong) {
  color: #764ba2;
  font-weight: 600;
}

/* ========== 过渡动画 ========== */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .title-card,
  .form-card,
  .analysis-form-card,
  .hexagram-card,
  .result-section {
    padding: 24px;
    border-radius: 16px;
  }

  .title-icon {
    font-size: 48px;
  }

  .page-title {
    font-size: 28px;
  }

  .page-subtitle {
    font-size: 14px;
  }

  .hexagram-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .button-group {
    flex-direction: column;
  }

  .analyze-btn,
  .reset-btn {
    flex: 1;
  }
}

@media (max-width: 480px) {
  .title-card,
  .form-card,
  .analysis-form-card,
  .hexagram-card,
  .result-section {
    padding: 20px;
  }

  .title-icon {
    font-size: 40px;
  }

  .page-title {
    font-size: 24px;
  }

  .hexagram-value.main-gua {
    font-size: 24px;
  }

  .hexagram-value.change-gua {
    font-size: 20px;
  }

  .submit-btn,
  .analyze-btn,
  .reset-btn {
    height: 44px;
    font-size: 15px;
  }
}
</style>
