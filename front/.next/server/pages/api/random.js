"use strict";
/*
 * ATTENTION: An "eval-source-map" devtool has been used.
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file with attached SourceMaps in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(() => {
var exports = {};
exports.id = "pages/api/random";
exports.ids = ["pages/api/random"];
exports.modules = {

/***/ "(api)/./pages/api/random.js":
/*!*****************************!*\
  !*** ./pages/api/random.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ handler)\n/* harmony export */ });\nfunction handler(req, res) {\n    // 生成一个1到100之间的随机数\n    const randomNumber = Math.floor(Math.random() * 100) + 1;\n    // 返回随机数据\n    res.status(200).json({\n        number: randomNumber,\n        message: `这是一个1到100之间的随机数: ${randomNumber}`\n    });\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvcmFuZG9tLmpzLmpzIiwibWFwcGluZ3MiOiI7Ozs7QUFBZSxTQUFTQSxPQUFPLENBQUNDLEdBQUcsRUFBRUMsR0FBRyxFQUFFO0lBQ3hDLGtCQUFrQjtJQUNsQixNQUFNQyxZQUFZLEdBQUdDLElBQUksQ0FBQ0MsS0FBSyxDQUFDRCxJQUFJLENBQUNFLE1BQU0sRUFBRSxHQUFHLEdBQUcsQ0FBQyxHQUFHLENBQUM7SUFFeEQsU0FBUztJQUNUSixHQUFHLENBQUNLLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQ0MsSUFBSSxDQUFDO1FBQ25CQyxNQUFNLEVBQUVOLFlBQVk7UUFDcEJPLE9BQU8sRUFBRSxDQUFDLGlCQUFpQixFQUFFUCxZQUFZLENBQUMsQ0FBQztLQUM1QyxDQUFDO0FBQ0osQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL215LW5leHRqcy1hcHAvLi9wYWdlcy9hcGkvcmFuZG9tLmpzP2ZlOWMiXSwic291cmNlc0NvbnRlbnQiOlsiZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gaGFuZGxlcihyZXEsIHJlcykge1xuICAvLyDnlJ/miJDkuIDkuKox5YiwMTAw5LmL6Ze055qE6ZqP5py65pWwXG4gIGNvbnN0IHJhbmRvbU51bWJlciA9IE1hdGguZmxvb3IoTWF0aC5yYW5kb20oKSAqIDEwMCkgKyAxXG5cbiAgLy8g6L+U5Zue6ZqP5py65pWw5o2uXG4gIHJlcy5zdGF0dXMoMjAwKS5qc29uKHsgXG4gICAgbnVtYmVyOiByYW5kb21OdW1iZXIsXG4gICAgbWVzc2FnZTogYOi/meaYr+S4gOS4qjHliLAxMDDkuYvpl7TnmoTpmo/mnLrmlbA6ICR7cmFuZG9tTnVtYmVyfWBcbiAgfSlcbn0iXSwibmFtZXMiOlsiaGFuZGxlciIsInJlcSIsInJlcyIsInJhbmRvbU51bWJlciIsIk1hdGgiLCJmbG9vciIsInJhbmRvbSIsInN0YXR1cyIsImpzb24iLCJudW1iZXIiLCJtZXNzYWdlIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(api)/./pages/api/random.js\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/random.js"));
module.exports = __webpack_exports__;

})();