<template>
  <div class="home-container">
    <a-card class="w-full max-w-2xl mx-auto rounded-lg shadow-xl custom-card" hoverable>
      <template #title>
        <div class="card-title">
          <h2 class="text-3xl font-extrabold text-indigo-700 mb-2 drop-shadow">问天易经智能体</h2>
          <p class="text-md text-gray-500 tracking-wide">解密命理玄机，预见未来之路</p>
        </div>
      </template>
      <div class="prose text-gray-700 leading-relaxed">
        <p class="text-lg intro-text">
          欢迎踏入问天易经智能体的奇妙世界！在这里，我们融合了古老的东方智慧与尖端的人工智能技术，为你开启一场探索自我、洞察未来的旅程。准备好迎接“易经+大模型”带来的震撼体验了吗？
        </p>

        <h4 class="text-xl font-semibold mt-6 mb-3 text-indigo-800 section-title">技术亮点</h4>
        <ul class="tech-list">
          <li class="tech-item">
            <span class="tech-icon"><i class="iconfont icon-jishuzhichi"></i></span>
            <div class="tech-content">
              <strong class="tech-name">实现原理：</strong>
              <p>
                我们融合了<strong>传统易经算法</strong>、<strong>LangChain框架</strong>以及<strong>通义千问Qwen3大模型</strong>，
                打造了智能、精准的易经命理分析系统。
              </p>
              <ul>
                <li>
                  <strong>易经经典算法：</strong> 核心计算公式来源于《周易》、《易经正义》等经典著作，确保传统命理学的严谨性和准确性。
                </li>
                <li>
                  <strong>LangChain智能链：</strong> 采用LangChain框架构建AI推理链路，实现易经知识的结构化处理和智能问答。
                </li>
                <li>
                  <strong>千问3深度解读：</strong> 集成通义千问Qwen3大模型，对卦象进行深度语义理解，提供富有哲理的个性化解读和建议。
                </li>
                <li>
                  <strong>提示词工程：</strong> 精心设计的易经分析提示模板，确保AI输出符合传统易学精神和现代实用价值。
                </li>
              </ul>
            </div>
          </li>
        </ul>

        <h4 class="text-xl font-semibold mt-6 mb-3 text-indigo-800 section-title">功能亮点</h4>
        <ul class="feature-list">
          <li class="feature-item">
            <span class="feature-icon"><i class="iconfont icon-bazicehuan"></i></span>
            <div class="feature-content">
              <strong class="feature-name">八字乾坤</strong>：只需提供你的出生日期和性别，瞬间为你展开一幅精妙的八字命盘。
              我们将深入剖析你的五行属性，揭示潜在的运势密码，为你的人生走向提供个性化的建议和指引。不再盲目摸索，让命运掌握在自己手中！
            </div>
          </li>
          <li class="feature-item">
            <span class="feature-icon"><i class="iconfont icon-qiguaizhanbu"></i></span>
            <div class="feature-content">
              <strong class="feature-name">六爻神卜</strong>：心怀疑惑，不知所向？ 通过神秘的易经六爻占卜，为你拨开迷雾，指点迷津。
              无论是事业、爱情还是财运，我们将为你解读卦象，洞察未来趋势，助你做出明智的决策，趋吉避凶，成就辉煌人生！
            </div>
          </li>
        </ul>

        <p class="call-to-action">
          还在犹豫什么？点击顶部导航栏，即刻开启你的专属命理探索之旅！让问天易经智能体成为你人生道路上的智慧伙伴，助你把握机遇，迎接挑战，创造属于自己的精彩篇章！
        </p>
      </div>
    </a-card>

    <!-- 免责声明 -->
    <div class="disclaimer">
      <h3 class="font-semibold mb-2">免责声明</h3>
      <p>
        本网站提供的所有易经、命理、风水、占卜等相关信息，仅供娱乐参考，不可作为任何决策的依据。
      </p>
      <p>
        本站内容，包括但不限于文字、图片、音频、视频等，均不构成任何形式的建议或保证。对于因使用本网站信息而产生的任何后果，本站概不负责。
      </p>
      <p>
        请您在使用本站信息时，保持理性和审慎的态度，切勿迷信。命运掌握在自己手中，请相信科学，积极面对生活。
      </p>
      <p>
        本站不对信息的准确性、完整性、及时性做出任何承诺。 任何依赖本站信息的行为，均由您个人承担风险。
      </p>
      <p>感谢您的理解与支持！</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
};
</script>

<style scoped>
@import "//at.alicdn.com/t/c/font_4413711_q2o769l1v3.css";

.home-container {
  padding: 30px;
  background: linear-gradient(to bottom, #f0f4ff, #ffffff); /* 渐变背景 */
}

.custom-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 添加过渡效果 */
}

.custom-card:hover {
  transform: translateY(-5px); /* 悬停时向上微移 */
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15); /* 加强阴影效果 */
}

.card-title {
  text-align: center;
}

.intro-text {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 20px;
}

.section-title {
  position: relative;
  padding-bottom: 10px;
  margin-bottom: 20px;
}

.section-title::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  width: 50px;
  height: 3px;
  background-color: #9fa8da; /* 分割线颜色 */
  border-radius: 2px;
}

.feature-list {
  list-style: none;
  padding: 0;
}

.feature-item {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  padding: 15px;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.7); /* 半透明背景 */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08); /* 轻微阴影 */
  transition: background-color 0.3s ease; /* 添加过渡效果 */
}

.feature-item:hover {
  background-color: rgba(255, 255, 255, 0.9); /* 悬停时加深背景色 */
}

.feature-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #e8eaf6;
  color: #5c6bc0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  margin-right: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08); /* 图标阴影 */
}

.feature-content {
  flex: 1;
}

.feature-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #3f51b5;
  margin-bottom: 5px;
  display: block;
}

.feature-description {
  color: #777;
}

.call-to-action {
  font-size: 1.1rem;
  text-align: center;
  margin-top: 30px;
  color: #666;
}

/* 免责声明样式 */
.disclaimer {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
  margin-top: 2rem;
  text-align: center;
  color: red;
  font-size: 0.75rem;
}

.disclaimer h3 {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.disclaimer p {
  margin-bottom: 0.25rem;
}

/* 技术亮点样式 */
.tech-list {
  list-style: none;
  padding: 0;
}

.tech-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 25px;
  padding: 15px;
  border-radius: 10px;
  background-color: rgba(240, 244, 255, 0.7); /* 浅色背景 */
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.tech-icon {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #d1c4e9; /* 浅紫色 */
  color: #673ab7; /* 深紫色 */
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  margin-right: 20px;
}

.tech-content {
  flex: 1;
}

.tech-content ul {
  list-style: disc;
  padding-left: 20px;
  margin-top: 10px;
}

.tech-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #5e35b1; /* 深紫色 */
  margin-bottom: 5px;
}
</style>
