// Cấu hình Allure Report
export default {
  name: "Bank Account - Test Report",
  output: "./allure-report",
  plugins: {
    awesome: {
      options: {
        reportName: "Bank Account - Test Report",
        groupBy: ["feature"],
      },
    },
  },
};