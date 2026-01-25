<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-icon">☯</div>
        <h1 class="hero-title">问天易经智能体</h1>
        <p class="hero-subtitle">让千年智慧遇见现代AI，古为今用，问道未来</p>
        <div class="hero-tags">
          <span class="tag">传统易经算法</span>
          <span class="tag">LangChain框架</span>
          <span class="tag">通义千问Qwen3</span>
        </div>
      </div>
    </section>

    <!-- 功能卡片 -->
    <section class="features-section">
      <h2 class="section-title">核心功能</h2>
      <div class="feature-grid">
        <div class="feature-card" @click="goToBazi">
          <div class="feature-card-icon bagua-icon">
            <div class="icon-inner">☯</div>
            <div class="icon-subtitle">八字</div>
          </div>
          <h3 class="feature-card-title">八字乾坤</h3>
          <p class="feature-card-desc">
            只需提供出生日期和性别，瞬间为你展开精妙的八字命盘。深入剖析五行属性，揭示潜在的运势密码，为人生走向提供个性化的建议和指引。
          </p>
          <div class="feature-card-tags">
            <span>排盘分析</span>
            <span>五行解读</span>
            <span>十神推演</span>
          </div>
          <div class="click-hint">点击进入 →</div>
        </div>

        <div class="feature-card" @click="goToGua">
          <div class="feature-card-icon trigram-icon">
            <div class="icon-inner">☷</div>
            <div class="icon-subtitle">占卜</div>
          </div>
          <h3 class="feature-card-title">六爻神卜</h3>
          <p class="feature-card-desc">
            通过神秘的易经六爻占卜，为你拨开迷雾，指点迷津。无论是事业、爱情还是财运，解读卦象，洞察未来趋势，助你做出明智的决策。
          </p>
          <div class="feature-card-tags">
            <span>64卦占卜</span>
            <span>卦象解析</span>
            <span>吉凶预测</span>
          </div>
          <div class="click-hint">点击进入 →</div>
        </div>
      </div>
    </section>

    <!-- 技术亮点 -->
    <section class="tech-section">
      <h2 class="section-title">技术亮点</h2>
      <div class="tech-grid">
        <div class="tech-card">
          <div class="tech-card-header">
            <div class="tech-card-icon">📚</div>
            <h3>易经经典算法</h3>
          </div>
          <p>核心计算公式来源于《周易》、《易经正义》等经典著作，确保传统命理学的严谨性和准确性。</p>
        </div>

        <div class="tech-card">
          <div class="tech-card-header">
            <div class="tech-card-icon">🔗</div>
            <h3>LangChain智能链</h3>
          </div>
          <p>采用LangChain框架构建AI推理链路，实现易经知识的结构化处理和智能问答。</p>
        </div>

        <div class="tech-card">
          <div class="tech-card-header">
            <div class="tech-card-icon">🤖</div>
            <h3>千问3深度解读</h3>
          </div>
          <p>集成通义千问Qwen3大模型，对卦象进行深度语义理解，提供富有哲理的个性化解读。</p>
        </div>

        <div class="tech-card">
          <div class="tech-card-header">
            <div class="tech-card-icon">✨</div>
            <h3>提示词工程</h3>
          </div>
          <p>精心设计的易经分析提示模板，确保AI输出符合传统易学精神和现代实用价值。</p>
        </div>
      </div>
    </section>

    <!-- GitHub 开源 -->
    <section class="github-section">
      <div class="github-card">
        <div class="github-icon">⭐</div>
        <h3>开源免费项目</h3>
        <p>本项目开源免费，代码托管在 GitHub 上，欢迎 Star 和贡献代码</p>
        <a
          href="https://github.com/timmy1688/wtian"
          target="_blank"
          rel="noopener noreferrer"
          class="github-button"
        >
          <svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
          </svg>
          访问 GitHub 项目
        </a>
      </div>
    </section>

    <!-- 免责声明 -->
    <section class="disclaimer-section">
      <div class="disclaimer-card">
        <h3>⚠️ 免责声明</h3>
        <div class="disclaimer-content">
          <p>本网站提供的所有易经、命理、风水、占卜等相关信息，<strong>仅供娱乐参考</strong>，不可作为任何决策的依据。</p>
          <p>本站内容均不构成任何形式的建议或保证。对于因使用本网站信息而产生的任何后果，本站概不负责。</p>
          <p>请您在使用本站信息时，保持理性和审慎的态度，切勿迷信。<strong>命运掌握在自己手中</strong>，请相信科学，积极面对生活。</p>
          <p class="disclaimer-note">感谢您的理解与支持！</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  name: 'HomeView',
  setup() {
    const router = useRouter();

    const goToBazi = () => {
      router.push({ name: 'Bazi' });
    };

    const goToGua = () => {
      router.push({ name: 'Gua' });
    };

    return {
      goToBazi,
      goToGua
    };
  }
};
</script>

<style scoped>
.home-container {
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

/* ========== Hero Section ========== */
.hero-section {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 24px;
  padding: 60px 40px;
  margin-bottom: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
  animation: pulse 15s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-icon {
  font-size: 80px;
  margin-bottom: 20px;
  animation: rotate 30s linear infinite;
  display: inline-block;
}

.hero-title {
  font-size: 42px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
  line-height: 1.6;
}

.hero-tags {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.hero-tags .tag {
  display: inline-block;
  padding: 8px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.hero-tags .tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

/* ========== Section Title ========== */
.section-title {
  font-size: 32px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

/* ========== Features Section ========== */
.features-section {
  margin-bottom: 60px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.4s ease;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.3);
}

.feature-card:active {
  transform: translateY(-5px);
}

.feature-card-icon {
  position: relative;
  margin-bottom: 20px;
  height: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.feature-card-icon .icon-inner {
  font-size: 60px;
  display: inline-block;
  position: relative;
}

.feature-card-icon .icon-subtitle {
  font-size: 14px;
  font-weight: 600;
  color: #667eea;
  margin-top: 8px;
  letter-spacing: 2px;
}

/* 八字图标特效 - 太极旋转 */
.bagua-icon .icon-inner {
  animation: rotate 20s linear infinite;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 八卦图标特效 */
.trigram-icon .icon-inner {
  color: #764ba2;
  animation: pulse 3s ease-in-out infinite;
}

.feature-card-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.feature-card-desc {
  font-size: 15px;
  color: #666;
  line-height: 1.8;
  margin-bottom: 20px;
}

.feature-card-tags {
  display: flex;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.feature-card-tags span {
  padding: 6px 14px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

/* 点击提示 */
.click-hint {
  margin-top: 20px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 600;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s ease;
}

.feature-card:hover .click-hint {
  opacity: 1;
  transform: translateY(0);
}

/* ========== Tech Section ========== */
.tech-section {
  margin-bottom: 60px;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.tech-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.tech-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.15);
}

.tech-card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.tech-card-icon {
  font-size: 32px;
}

.tech-card h3 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.tech-card p {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
  margin: 0;
}

/* ========== GitHub Section ========== */
.github-section {
  margin-bottom: 40px;
}

.github-card {
  background: linear-gradient(135deg, #24292e 0%, #1a1a1a 100%);
  border-radius: 20px;
  padding: 50px 40px;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.github-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
}

.github-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.github-card h3 {
  font-size: 28px;
  font-weight: 700;
  color: white;
  margin-bottom: 12px;
}

.github-card p {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 30px;
  line-height: 1.6;
}

.github-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 32px;
  background: white;
  color: #24292e;
  text-decoration: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 16px rgba(255, 255, 255, 0.2);
  position: relative;
  z-index: 1;
}

.github-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

/* ========== Disclaimer Section ========== */
.disclaimer-section {
  margin-bottom: 20px;
}

.disclaimer-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 30px;
  border-left: 4px solid #ff6b6b;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.disclaimer-card h3 {
  font-size: 20px;
  font-weight: 700;
  color: #ff6b6b;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.disclaimer-content {
  font-size: 14px;
  color: #666;
  line-height: 1.8;
}

.disclaimer-content p {
  margin-bottom: 12px;
}

.disclaimer-content strong {
  color: #ff6b6b;
  font-weight: 600;
}

.disclaimer-note {
  font-weight: 600;
  color: #333;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

/* ========== 响应式设计 ========== */
@media (max-width: 768px) {
  .hero-section {
    padding: 40px 24px;
    border-radius: 16px;
  }

  .hero-icon {
    font-size: 60px;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .section-title {
    font-size: 26px;
  }

  .feature-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .feature-card {
    padding: 30px 20px;
  }

  .feature-card-icon {
    height: 80px;
  }

  .feature-card-icon .icon-inner {
    font-size: 50px;
  }

  .tech-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .github-card {
    padding: 40px 24px;
    border-radius: 16px;
  }

  .github-icon {
    font-size: 50px;
  }

  .github-card h3 {
    font-size: 24px;
  }

  .disclaimer-card {
    padding: 24px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 30px 20px;
  }

  .hero-icon {
    font-size: 50px;
  }

  .feature-card-icon {
    height: 70px;
  }

  .feature-card-icon .icon-inner {
    font-size: 45px;
  }

  .hero-title {
    font-size: 26px;
  }

  .hero-subtitle {
    font-size: 14px;
  }

  .hero-tags {
    gap: 8px;
  }

  .hero-tags .tag {
    font-size: 12px;
    padding: 6px 14px;
  }

  .section-title {
    font-size: 22px;
  }

  .feature-card-title {
    font-size: 20px;
  }

  .github-button {
    padding: 12px 24px;
    font-size: 14px;
  }
}
</style>
