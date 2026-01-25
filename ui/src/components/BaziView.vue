<template>
  <div class="bazi-container">
    <!-- 标题卡片 -->
    <div class="title-card">
      <div class="title-icon">☯</div>
      <h1 class="page-title">八字排盘</h1>
      <p class="page-subtitle">输入出生信息，AI 为你解析命理玄机</p>
    </div>

    <!-- 输入表单 -->
    <div class="form-card">
      <a-form :model="baziInput" layout="vertical">
        <!-- 日历类型 -->
        <a-form-item label="日历类型">
          <a-radio-group v-model:value="is_lunar" @change="onCalendarTypeChange" size="large">
            <a-radio-button :value="false">公历</a-radio-button>
            <a-radio-button :value="true">农历</a-radio-button>
          </a-radio-group>
        </a-form-item>

        <!-- 出生日期 -->
        <a-form-item :label="is_lunar ? '出生日期 (农历)' : '出生日期 (公历)'">
          <a-date-picker
            v-model:value="birthDate"
            show-time
            format="YYYY-MM-DD HH"
            @change="onBirthDateChange"
            size="large"
            :locale="locale"
            placeholder="请选择出生日期和时辰"
            style="width: 100%"
          />
        </a-form-item>

        <!-- 性别 -->
        <a-form-item label="性别">
          <a-radio-group v-model:value="baziInput.gender" size="large">
            <a-radio-button value="boy">男</a-radio-button>
            <a-radio-button value="girl">女</a-radio-button>
          </a-radio-group>
        </a-form-item>

        <!-- 排盘按钮 -->
        <a-form-item>
          <a-button 
            type="primary" 
            @click="fetchBazi" 
            :loading="loadingBazi"
            size="large"
            block
            class="submit-btn"
          >
            <template v-if="!loadingBazi">开始排盘</template>
            <template v-else>排盘中...</template>
          </a-button>
        </a-form-item>
      </a-form>
    </div>

    <!-- 八字结果 -->
    <transition name="fade-slide">
      <div v-if="baziResult" class="result-section">
        <div class="result-header">
          <h2 class="result-title">排盘结果</h2>
        </div>

        <div class="result-grid">
          <div class="result-item">
            <div class="result-label">公历</div>
            <div class="result-value">{{ baziResult.new_birth }}</div>
          </div>
          <div class="result-item">
            <div class="result-label">农历</div>
            <div class="result-value">{{ baziResult.old_birth }}</div>
          </div>
          <div class="result-item full-width">
            <div class="result-label">八字</div>
            <div class="result-value bazi-chars">
              <span v-for="(char, index) in baziResult.bazi" :key="index" class="bazi-char">
                {{ char }}
              </span>
            </div>
          </div>
          <div class="result-item full-width">
            <div class="result-label">十神</div>
            <div class="result-value bazi-chars">
              <span v-for="(god, index) in baziResult.shishen" :key="index" class="shishen-char">
                {{ god }}
              </span>
            </div>
          </div>
          <div class="result-item full-width">
            <div class="result-label">五行分布</div>
            <div class="wuxing-container">
              <div v-for="(value, key) in baziResult.wuxing" :key="key" class="wuxing-item">
                <div class="wuxing-label">{{ key }}</div>
                <div class="wuxing-bar">
                  <div 
                    class="wuxing-fill" 
                    :style="{ width: value + '%' }"
                    :class="'wuxing-' + key"
                  ></div>
                </div>
                <div class="wuxing-value">{{ value }}%</div>
              </div>
            </div>
          </div>
        </div>

        <div class="action-center">
          <a-button 
            type="primary" 
            @click="fetchFenxi" 
            :loading="loadingFenxi"
            size="large"
            class="analyze-btn"
          >
            <template v-if="!loadingFenxi">AI 智能分析</template>
            <template v-else>分析中...</template>
          </a-button>
        </div>
      </div>
    </transition>

    <!-- 分析结果 -->
    <transition name="fade-slide">
      <div v-if="fenxiResult" class="analysis-section">
        <div class="analysis-header">
          <h2 class="analysis-title">命盘分析</h2>
        </div>
        <div class="analysis-content">
          <div class="markdown-body" v-html="renderedMarkdown"></div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import axios from 'axios';
import { message } from 'ant-design-vue';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';
import customParseFormat from 'dayjs/plugin/customParseFormat';
import zhCN from 'ant-design-vue/es/date-picker/locale/zh_CN';
import MarkdownIt from 'markdown-it';
import { API_BASE_URL } from '../api/config';

dayjs.extend(customParseFormat);
dayjs.locale('zh-cn');

export default {
  name: 'BaziView',
  setup() {
    const baziInput = ref({ birth: '', gender: 'boy', is_lunar: false });
    const birthDate = ref(null);
    const baziResult = ref(null);
    const fenxiResult = ref(null);
    const loadingBazi = ref(false);
    const loadingFenxi = ref(false);
    const locale = ref(zhCN);
    const is_lunar = ref(false);

    const onCalendarTypeChange = (e) => {
      baziInput.value.is_lunar = e.target.value;
    };

    const onBirthDateChange = (date, dateString) => {
      if (dateString) {
        const formattedDate = dayjs(date);
        const hour = formattedDate.format('HH');
        const datePart = formattedDate.format('YYYYMMDD');
        baziInput.value.birth = `${datePart} ${hour}`;
      } else {
        baziInput.value.birth = '';
      }
    };

    const fetchBazi = async () => {
      loadingBazi.value = true;

      if (!baziInput.value.birth || !baziInput.value.gender) {
        message.error('请填写完整的出生日期和性别信息！');
        loadingBazi.value = false;
        return;
      }

      try {
        const response = await axios.post(`${API_BASE_URL}/bazi/paipan`, {
          birth: baziInput.value.birth,
          gender: baziInput.value.gender,
          is_lunar: baziInput.value.is_lunar
        });

        if (response.data && typeof response.data === 'object') {
          baziResult.value = response.data;
          message.success('排盘成功！');
        } else {
          message.error('服务器返回数据格式错误！');
          baziResult.value = null;
        }
        fenxiResult.value = null;
      } catch (error) {
        console.error('Error during fetchBazi:', error);
        message.error('排盘失败，请检查输入！');
      } finally {
        loadingBazi.value = false;
      }
    };

    const fetchFenxi = async () => {
      loadingFenxi.value = true;
      try {
        const response = await axios.post(`${API_BASE_URL}/bazi/fenxi`, {
          gender: baziResult.value.gender,
          bazi: baziResult.value.bazi,
          shishen: baziResult.value.shishen,
          wuxing: baziResult.value.wuxing,
          demand: '无',
        });

        if (response.data.status === 'success') {
          fenxiResult.value = response.data;
          message.success('分析完成！');
        } else if (response.data.status === 'limited') {
          message.warning(response.data.message);
        } else {
          message.error('分析失败！');
        }
      } catch (error) {
        message.error('分析失败！');
      } finally {
        loadingFenxi.value = false;
      }
    };

    const md = new MarkdownIt();

    const renderedMarkdown = computed(() => {
      if (fenxiResult.value && fenxiResult.value.result) {
        return md.render(fenxiResult.value.result);
      }
      return '';
    });

    return {
      baziInput,
      birthDate,
      baziResult,
      fenxiResult,
      loadingBazi,
      loadingFenxi,
      is_lunar,
      onCalendarTypeChange,
      onBirthDateChange,
      fetchBazi,
      fetchFenxi,
      renderedMarkdown,
      locale,
    };
  },
};
</script>

<style scoped>
.bazi-container {
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
  animation: rotate 20s linear infinite;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
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
.form-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.form-card :deep(.ant-form-item-label > label) {
  font-weight: 600;
  font-size: 15px;
  color: #333;
}

.form-card :deep(.ant-radio-button-wrapper) {
  border-radius: 8px;
  border: 2px solid #e0e0e0;
  margin-right: 12px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.form-card :deep(.ant-radio-button-wrapper:hover) {
  border-color: #667eea;
}

.form-card :deep(.ant-radio-button-wrapper-checked) {
  border-color: #667eea !important;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.form-card :deep(.ant-picker) {
  border-radius: 12px;
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.form-card :deep(.ant-picker:hover),
.form-card :deep(.ant-picker-focused) {
  border-color: #667eea;
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

/* ========== Result Section ========== */
.result-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 30px;
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

.result-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.result-item {
  background: rgba(102, 126, 234, 0.05);
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
}

.result-item:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.result-item.full-width {
  grid-column: 1 / -1;
}

.result-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
  font-weight: 500;
}

.result-value {
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.bazi-chars {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.bazi-char,
.shishen-char {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  font-size: 20px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.bazi-char:hover,
.shishen-char:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* ========== 五行分布 ========== */
.wuxing-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.wuxing-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.wuxing-label {
  min-width: 40px;
  font-weight: 600;
  font-size: 14px;
  color: #333;
}

.wuxing-bar {
  flex: 1;
  height: 28px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 14px;
  overflow: hidden;
  position: relative;
}

.wuxing-fill {
  height: 100%;
  border-radius: 14px;
  transition: width 0.8s ease;
  position: relative;
  overflow: hidden;
}

.wuxing-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.wuxing-木 {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.wuxing-火 {
  background: linear-gradient(90deg, #ef4444, #f87171);
}

.wuxing-土 {
  background: linear-gradient(90deg, #f59e0b, #fbbf24);
}

.wuxing-金 {
  background: linear-gradient(90deg, #6b7280, #9ca3af);
}

.wuxing-水 {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.wuxing-value {
  min-width: 50px;
  text-align: right;
  font-weight: 600;
  font-size: 14px;
  color: #667eea;
}

.action-center {
  text-align: center;
}

.analyze-btn {
  height: 50px;
  padding: 0 48px;
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

/* ========== Analysis Section ========== */
.analysis-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.analysis-header {
  text-align: center;
  margin-bottom: 32px;
}

.analysis-title {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.analysis-content {
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
}

.markdown-body :deep(p) {
  margin-bottom: 16px;
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
  .result-section,
  .analysis-section {
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

  .result-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .bazi-chars {
    gap: 12px;
  }

  .bazi-char,
  .shishen-char {
    min-width: 50px;
    height: 50px;
    font-size: 18px;
  }

  .wuxing-item {
    flex-direction: column;
    align-items: stretch;
  }

  .wuxing-label {
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .title-card,
  .form-card,
  .result-section,
  .analysis-section {
    padding: 20px;
  }

  .title-icon {
    font-size: 40px;
  }

  .page-title {
    font-size: 24px;
  }

  .bazi-chars {
    gap: 8px;
  }

  .bazi-char,
  .shishen-char {
    min-width: 45px;
    height: 45px;
    font-size: 16px;
  }

  .submit-btn,
  .analyze-btn {
    height: 44px;
    font-size: 15px;
  }
}
</style>
