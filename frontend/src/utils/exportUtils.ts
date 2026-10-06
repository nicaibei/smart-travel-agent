/**
 * 导出功能 - 图片和PDF
 */

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { message } from 'ant-design-vue';
import type { TripPlan } from '@/types';

// ===================================
// 1. 导出为图片
// ===================================

/**
 * 导出旅行计划为PNG图片
 * @param elementId 要导出的DOM元素ID
 * @param tripPlan 旅行计划数据（用于文件名）
 */
export const exportAsImage = async (
  elementId: string = 'trip-plan-content',
  tripPlan?: TripPlan
) => {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      message.error('未找到要导出的内容');
      return;
    }

    // 显示加载提示
    const hideLoading = message.loading('正在生成图片...', 0);

    // 使用html2canvas截取DOM
    const canvas = await html2canvas(element, {
      backgroundColor: '#ffffff',
      scale: 2, // 2倍分辨率，更清晰
      useCORS: true, // 允许跨域图片
      allowTaint: false,
      logging: false,
      imageTimeout: 0,
      // 优化配置
      windowWidth: element.scrollWidth,
      windowHeight: element.scrollHeight,
    });

    hideLoading();

    // 创建下载链接
    const link = document.createElement('a');
    const fileName = tripPlan
      ? `${tripPlan.city}旅行计划_${tripPlan.start_date}.png`
      : '旅行计划.png';
    
    link.download = fileName;
    link.href = canvas.toDataURL('image/png', 1.0);
    link.click();

    message.success('图片导出成功！');
  } catch (error) {
    console.error('导出图片失败:', error);
    message.error('导出图片失败，请重试');
  }
};


// ===================================
// 2. 导出为PDF
// ===================================

/**
 * 导出旅行计划为PDF
 * @param elementId 要导出的DOM元素ID
 * @param tripPlan 旅行计划数据
 */
export const exportAsPDF = async (
  elementId: string = 'trip-plan-content',
  tripPlan?: TripPlan
) => {
  try {
    const element = document.getElementById(elementId);
    if (!element) {
      message.error('未找到要导出的内容');
      return;
    }

    // 显示加载提示
    const hideLoading = message.loading('正在生成PDF...', 0);

    // 截取DOM为Canvas
    const canvas = await html2canvas(element, {
      backgroundColor: '#ffffff',
      scale: 2,
      useCORS: true,
      allowTaint: true,
      logging: false,
      imageTimeout: 0,
    });

    hideLoading();

    // 创建PDF
    const pdf = new jsPDF({
      orientation: 'portrait', // 纵向
      unit: 'mm',
      format: 'a4',
    });

    // 获取图片数据
    const imgData = canvas.toDataURL('image/png', 1.0);
    
    // A4尺寸（单位：mm）
    const pdfWidth = 210;
    const pdfHeight = 297;
    
    // 计算图片在PDF中的尺寸（保持宽高比）
    const imgWidth = pdfWidth;
    const imgHeight = (canvas.height * pdfWidth) / canvas.width;

    // 如果内容高度超过一页，分页处理
    if (imgHeight > pdfHeight) {
      let position = 0;
      const pageHeight = (canvas.width * pdfHeight) / pdfWidth;
      
      while (position < canvas.height) {
        // 创建临时canvas，只包含当前页内容
        const pageCanvas = document.createElement('canvas');
        pageCanvas.width = canvas.width;
        pageCanvas.height = Math.min(pageHeight, canvas.height - position);
        
        const ctx = pageCanvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(
            canvas,
            0,
            position,
            canvas.width,
            pageCanvas.height,
            0,
            0,
            canvas.width,
            pageCanvas.height
          );
          
          const pageImgData = pageCanvas.toDataURL('image/png', 1.0);
          
          if (position > 0) {
            pdf.addPage();
          }
          
          pdf.addImage(pageImgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
        }
        
        position += pageHeight;
      }
    } else {
      // 单页内容，直接添加
      pdf.addImage(imgData, 'PNG', 0, 0, imgWidth, imgHeight);
    }

    // 保存PDF
    const fileName = tripPlan
      ? `${tripPlan.city}旅行计划_${tripPlan.start_date}.pdf`
      : '旅行计划.pdf';
    
    pdf.save(fileName);

    message.success('PDF导出成功！');
  } catch (error) {
    console.error('导出PDF失败:', error);
    message.error('导出PDF失败，请重试');
  }
};


// ===================================
// 3. 优化的PDF导出（带封面和页眉页脚）
// ===================================

/**
 * 导出为带封面和格式化的PDF
 */
export const exportAsFormattedPDF = async (
  elementId: string,
  tripPlan: TripPlan
) => {
  try {
    const hideLoading = message.loading('正在生成精美PDF...', 0);

    const element = document.getElementById(elementId);
    if (!element) {
      message.error('未找到要导出的内容');
      return;
    }

    const canvas = await html2canvas(element, {
      backgroundColor: '#ffffff',
      scale: 2,
      useCORS: true,
      allowTaint: true,
    });

    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfWidth = 210;
    // 添加封面
    addCoverPage(pdf, tripPlan);

    // 添加新页面
    pdf.addPage();

    // 添加内容
    const imgData = canvas.toDataURL('image/png', 1.0);
    const imgWidth = pdfWidth - 20; // 留边距
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    
    pdf.addImage(imgData, 'PNG', 10, 20, imgWidth, imgHeight);

    // 添加页脚
    addFooter(pdf, tripPlan);

    hideLoading();

    pdf.save(`${tripPlan.city}旅行计划_${tripPlan.start_date}.pdf`);
    message.success('精美PDF导出成功！');
  } catch (error) {
    console.error('导出PDF失败:', error);
    message.error('导出PDF失败，请重试');
  }
};

// 添加封面
const addCoverPage = (pdf: jsPDF, tripPlan: TripPlan) => {
  pdf.setFillColor(102, 126, 234); // 渐变色
  pdf.rect(0, 0, 210, 297, 'F');

  // 标题
  pdf.setTextColor(255, 255, 255);
  pdf.setFontSize(32);
  pdf.text('旅行计划', 105, 100, { align: 'center' });

  // 城市名
  pdf.setFontSize(24);
  pdf.text(tripPlan.city, 105, 130, { align: 'center' });

  // 日期
  pdf.setFontSize(16);
  pdf.text(
    `${tripPlan.start_date} 至 ${tripPlan.end_date}`,
    105,
    150,
    { align: 'center' }
  );

  // 天数
  pdf.setFontSize(14);
  pdf.text(
    `${tripPlan.days.length} 天行程`,
    105,
    170,
    { align: 'center' }
  );
};

// 添加页脚
const addFooter = (pdf: jsPDF, tripPlan: TripPlan) => {
  const pageCount = pdf.getNumberOfPages();
  
  for (let i = 1; i <= pageCount; i++) {
    pdf.setPage(i);
    pdf.setFontSize(10);
    pdf.setTextColor(128, 128, 128);
    pdf.text(
      `${tripPlan.city}旅行计划 | 第 ${i} 页，共 ${pageCount} 页`,
      105,
      287,
      { align: 'center' }
    );
  }
};


// ===================================
// 4. 导出前的准备工作
// ===================================

/**
 * 隐藏地图和其他不需要导出的元素
 */
export const prepareForExport = (): (() => void) => {
  const elementsToHide = [
    '.amap-container', // 高德地图
    '.edit-buttons', // 编辑按钮
    '.action-buttons', // 操作按钮
    '.export-buttons', // 导出按钮
  ];

  const hiddenElements: HTMLElement[] = [];

  elementsToHide.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach(el => {
      const htmlEl = el as HTMLElement;
      if (htmlEl.style.display !== 'none') {
        htmlEl.style.display = 'none';
        hiddenElements.push(htmlEl);
      }
    });
  });

  // 返回恢复函数
  return () => {
    hiddenElements.forEach(el => {
      el.style.display = '';
    });
  };
};


// ===================================
// 5. 完整的导出流程
// ===================================

/**
 * 导出为图片（完整流程）
 */
export const exportImageWithPreparation = async (
  elementId: string,
  tripPlan?: TripPlan
) => {
  // 准备导出（隐藏不需要的元素）
  const restore = prepareForExport();

  try {
    // 等待DOM更新
    await new Promise(resolve => setTimeout(resolve, 100));
    
    // 导出
    await exportAsImage(elementId, tripPlan);
  } finally {
    // 恢复元素
    restore();
  }
};

/**
 * 导出为PDF（完整流程）
 */
export const exportPDFWithPreparation = async (
  elementId: string,
  tripPlan?: TripPlan
) => {
  const restore = prepareForExport();

  try {
    await new Promise(resolve => setTimeout(resolve, 100));
    await exportAsPDF(elementId, tripPlan);
  } finally {
    restore();
  }
};


// ===================================
// 6. 导出配置
// ===================================

export interface ExportOptions {
  elementId?: string;
  format: 'png' | 'pdf' | 'formatted-pdf';
  includeMap?: boolean;
  quality?: number; // 0-1
  scale?: number; // 1-3
}

/**
 * 通用导出函数
 */
export const exportTripPlan = async (
  tripPlan: TripPlan,
  options: ExportOptions = { format: 'png' }
) => {
  const elementId = options.elementId || 'trip-plan-content';

  switch (options.format) {
    case 'png':
      await exportImageWithPreparation(elementId, tripPlan);
      break;
    case 'pdf':
      await exportPDFWithPreparation(elementId, tripPlan);
      break;
    case 'formatted-pdf':
      await exportAsFormattedPDF(elementId, tripPlan);
      break;
    default:
      message.error('不支持的导出格式');
  }
};


// ===================================
// 使用示例
// ===================================

/*
在组件中使用：

<script setup lang="ts">
import { exportTripPlan } from '@/utils/exportUtils';

const tripPlan = ref<TripPlan>({ ... });

// 导出为图片
const handleExportImage = () => {
  exportTripPlan(tripPlan.value, { format: 'png' });
};

// 导出为PDF
const handleExportPDF = () => {
  exportTripPlan(tripPlan.value, { format: 'pdf' });
};

// 导出为精美PDF
const handleExportFormattedPDF = () => {
  exportTripPlan(tripPlan.value, { format: 'formatted-pdf' });
};
</script>

<template>
  <div>
    <!-- 导出按钮 -->
    <a-button @click="handleExportImage">导出图片</a-button>
    <a-button @click="handleExportPDF">导出PDF</a-button>
    
    <!-- 要导出的内容 -->
    <div id="trip-plan-content">
      <!-- 旅行计划内容 -->
    </div>
  </div>
</template>
*/
