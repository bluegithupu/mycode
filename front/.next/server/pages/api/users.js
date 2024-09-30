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
exports.id = "pages/api/users";
exports.ids = ["pages/api/users"];
exports.modules = {

/***/ "sqlite3":
/*!**************************!*\
  !*** external "sqlite3" ***!
  \**************************/
/***/ ((module) => {

module.exports = require("sqlite3");

/***/ }),

/***/ "util":
/*!***********************!*\
  !*** external "util" ***!
  \***********************/
/***/ ((module) => {

module.exports = require("util");

/***/ }),

/***/ "(api)/./lib/db.js":
/*!*******************!*\
  !*** ./lib/db.js ***!
  \*******************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"openDb\": () => (/* binding */ openDb)\n/* harmony export */ });\n/* harmony import */ var sqlite3__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! sqlite3 */ \"sqlite3\");\n/* harmony import */ var sqlite3__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(sqlite3__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var util__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! util */ \"util\");\n/* harmony import */ var util__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(util__WEBPACK_IMPORTED_MODULE_1__);\n\n\nlet db;\n// 初始化数据库\nfunction openDb() {\n    if (!db) {\n        db = new (sqlite3__WEBPACK_IMPORTED_MODULE_0___default().Database)(\"./mydb.sqlite\", (err)=>{\n            if (err) {\n                console.error(err.message);\n            }\n            console.log(\"Connected to the SQLite database.\");\n        });\n        db.run = (0,util__WEBPACK_IMPORTED_MODULE_1__.promisify)(db.run);\n        db.get = (0,util__WEBPACK_IMPORTED_MODULE_1__.promisify)(db.get);\n        db.all = (0,util__WEBPACK_IMPORTED_MODULE_1__.promisify)(db.all);\n        createTable();\n    }\n    return db;\n}\n// 创建用户表\nasync function createTable() {\n    const sql = `\n    CREATE TABLE IF NOT EXISTS users (\n      id INTEGER PRIMARY KEY AUTOINCREMENT,\n      name TEXT,\n      email TEXT UNIQUE\n    )\n  `;\n    try {\n        await db.run(sql);\n        console.log(\"Users table created or already exists.\");\n    } catch (err) {\n        console.error(\"Error creating users table:\", err.message);\n    }\n}\n\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9saWIvZGIuanMuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7QUFBNkI7QUFDRztBQUVoQyxJQUFJRSxFQUFFO0FBRU4sU0FBUztBQUNULFNBQVNDLE1BQU0sR0FBRztJQUNoQixJQUFJLENBQUNELEVBQUUsRUFBRTtRQUNQQSxFQUFFLEdBQUcsSUFBSUYseURBQWdCLENBQUMsZUFBZSxFQUFFLENBQUNLLEdBQUcsR0FBSztZQUNsRCxJQUFJQSxHQUFHLEVBQUU7Z0JBQ1BDLE9BQU8sQ0FBQ0MsS0FBSyxDQUFDRixHQUFHLENBQUNHLE9BQU8sQ0FBQztZQUM1QixDQUFDO1lBQ0RGLE9BQU8sQ0FBQ0csR0FBRyxDQUFDLG1DQUFtQyxDQUFDO1FBQ2xELENBQUMsQ0FBQztRQUNGUCxFQUFFLENBQUNRLEdBQUcsR0FBR1QsK0NBQVMsQ0FBQ0MsRUFBRSxDQUFDUSxHQUFHLENBQUM7UUFDMUJSLEVBQUUsQ0FBQ1MsR0FBRyxHQUFHViwrQ0FBUyxDQUFDQyxFQUFFLENBQUNTLEdBQUcsQ0FBQztRQUMxQlQsRUFBRSxDQUFDVSxHQUFHLEdBQUdYLCtDQUFTLENBQUNDLEVBQUUsQ0FBQ1UsR0FBRyxDQUFDO1FBQzFCQyxXQUFXLEVBQUU7SUFDZixDQUFDO0lBQ0QsT0FBT1gsRUFBRTtBQUNYLENBQUM7QUFFRCxRQUFRO0FBQ1IsZUFBZVcsV0FBVyxHQUFHO0lBQzNCLE1BQU1DLEdBQUcsR0FBRyxDQUFDOzs7Ozs7RUFNYixDQUFDO0lBQ0QsSUFBSTtRQUNGLE1BQU1aLEVBQUUsQ0FBQ1EsR0FBRyxDQUFDSSxHQUFHLENBQUM7UUFDakJSLE9BQU8sQ0FBQ0csR0FBRyxDQUFDLHdDQUF3QyxDQUFDO0lBQ3ZELEVBQUUsT0FBT0osR0FBRyxFQUFFO1FBQ1pDLE9BQU8sQ0FBQ0MsS0FBSyxDQUFDLDZCQUE2QixFQUFFRixHQUFHLENBQUNHLE9BQU8sQ0FBQztJQUMzRCxDQUFDO0FBQ0gsQ0FBQztBQUVnQiIsInNvdXJjZXMiOlsid2VicGFjazovL215LW5leHRqcy1hcHAvLi9saWIvZGIuanM/M2RjOSJdLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgc3FsaXRlMyBmcm9tICdzcWxpdGUzJ1xuaW1wb3J0IHsgcHJvbWlzaWZ5IH0gZnJvbSAndXRpbCdcblxubGV0IGRiXG5cbi8vIOWIneWni+WMluaVsOaNruW6k1xuZnVuY3Rpb24gb3BlbkRiKCkge1xuICBpZiAoIWRiKSB7XG4gICAgZGIgPSBuZXcgc3FsaXRlMy5EYXRhYmFzZSgnLi9teWRiLnNxbGl0ZScsIChlcnIpID0+IHtcbiAgICAgIGlmIChlcnIpIHtcbiAgICAgICAgY29uc29sZS5lcnJvcihlcnIubWVzc2FnZSlcbiAgICAgIH1cbiAgICAgIGNvbnNvbGUubG9nKCdDb25uZWN0ZWQgdG8gdGhlIFNRTGl0ZSBkYXRhYmFzZS4nKVxuICAgIH0pXG4gICAgZGIucnVuID0gcHJvbWlzaWZ5KGRiLnJ1bilcbiAgICBkYi5nZXQgPSBwcm9taXNpZnkoZGIuZ2V0KVxuICAgIGRiLmFsbCA9IHByb21pc2lmeShkYi5hbGwpXG4gICAgY3JlYXRlVGFibGUoKVxuICB9XG4gIHJldHVybiBkYlxufVxuXG4vLyDliJvlu7rnlKjmiLfooahcbmFzeW5jIGZ1bmN0aW9uIGNyZWF0ZVRhYmxlKCkge1xuICBjb25zdCBzcWwgPSBgXG4gICAgQ1JFQVRFIFRBQkxFIElGIE5PVCBFWElTVFMgdXNlcnMgKFxuICAgICAgaWQgSU5URUdFUiBQUklNQVJZIEtFWSBBVVRPSU5DUkVNRU5ULFxuICAgICAgbmFtZSBURVhULFxuICAgICAgZW1haWwgVEVYVCBVTklRVUVcbiAgICApXG4gIGBcbiAgdHJ5IHtcbiAgICBhd2FpdCBkYi5ydW4oc3FsKVxuICAgIGNvbnNvbGUubG9nKCdVc2VycyB0YWJsZSBjcmVhdGVkIG9yIGFscmVhZHkgZXhpc3RzLicpXG4gIH0gY2F0Y2ggKGVycikge1xuICAgIGNvbnNvbGUuZXJyb3IoJ0Vycm9yIGNyZWF0aW5nIHVzZXJzIHRhYmxlOicsIGVyci5tZXNzYWdlKVxuICB9XG59XG5cbmV4cG9ydCB7IG9wZW5EYiB9Il0sIm5hbWVzIjpbInNxbGl0ZTMiLCJwcm9taXNpZnkiLCJkYiIsIm9wZW5EYiIsIkRhdGFiYXNlIiwiZXJyIiwiY29uc29sZSIsImVycm9yIiwibWVzc2FnZSIsImxvZyIsInJ1biIsImdldCIsImFsbCIsImNyZWF0ZVRhYmxlIiwic3FsIl0sInNvdXJjZVJvb3QiOiIifQ==\n//# sourceURL=webpack-internal:///(api)/./lib/db.js\n");

/***/ }),

/***/ "(api)/./pages/api/users/index.js":
/*!**********************************!*\
  !*** ./pages/api/users/index.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ handler)\n/* harmony export */ });\n/* harmony import */ var _lib_db__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../lib/db */ \"(api)/./lib/db.js\");\n\nasync function handler(req, res) {\n    const db = (0,_lib_db__WEBPACK_IMPORTED_MODULE_0__.openDb)();\n    switch(req.method){\n        case \"GET\":\n            try {\n                const users = await db.all(\"SELECT * FROM users\");\n                res.status(200).json(users);\n            } catch (error) {\n                res.status(500).json({\n                    error: error.message\n                });\n            }\n            break;\n        case \"POST\":\n            const { name , email  } = req.body;\n            try {\n                // 修改这里：使用 get 方法来获取插入的 ID\n                await db.run(\"INSERT INTO users (name, email) VALUES (?, ?)\", [\n                    name,\n                    email\n                ]);\n                const result = await db.get(\"SELECT last_insert_rowid() as id\");\n                res.status(201).json({\n                    id: result.id,\n                    name,\n                    email\n                });\n            } catch (error1) {\n                res.status(400).json({\n                    error: error1.message\n                });\n            }\n            break;\n        default:\n            res.status(405).end() // Method Not Allowed\n            ;\n    }\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvdXNlcnMvaW5kZXguanMuanMiLCJtYXBwaW5ncyI6Ijs7Ozs7QUFBd0M7QUFFekIsZUFBZUMsT0FBTyxDQUFDQyxHQUFHLEVBQUVDLEdBQUcsRUFBRTtJQUM5QyxNQUFNQyxFQUFFLEdBQUdKLCtDQUFNLEVBQUU7SUFFbkIsT0FBUUUsR0FBRyxDQUFDRyxNQUFNO1FBQ2hCLEtBQUssS0FBSztZQUNSLElBQUk7Z0JBQ0YsTUFBTUMsS0FBSyxHQUFHLE1BQU1GLEVBQUUsQ0FBQ0csR0FBRyxDQUFDLHFCQUFxQixDQUFDO2dCQUNqREosR0FBRyxDQUFDSyxNQUFNLENBQUMsR0FBRyxDQUFDLENBQUNDLElBQUksQ0FBQ0gsS0FBSyxDQUFDO1lBQzdCLEVBQUUsT0FBT0ksS0FBSyxFQUFFO2dCQUNkUCxHQUFHLENBQUNLLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQ0MsSUFBSSxDQUFDO29CQUFFQyxLQUFLLEVBQUVBLEtBQUssQ0FBQ0MsT0FBTztpQkFBRSxDQUFDO1lBQ2hELENBQUM7WUFDRCxNQUFLO1FBRVAsS0FBSyxNQUFNO1lBQ1QsTUFBTSxFQUFFQyxJQUFJLEdBQUVDLEtBQUssR0FBRSxHQUFHWCxHQUFHLENBQUNZLElBQUk7WUFDaEMsSUFBSTtnQkFDRiwwQkFBMEI7Z0JBQzFCLE1BQU1WLEVBQUUsQ0FBQ1csR0FBRyxDQUNWLCtDQUErQyxFQUMvQztvQkFBQ0gsSUFBSTtvQkFBRUMsS0FBSztpQkFBQyxDQUNkO2dCQUNELE1BQU1HLE1BQU0sR0FBRyxNQUFNWixFQUFFLENBQUNhLEdBQUcsQ0FBQyxrQ0FBa0MsQ0FBQztnQkFDL0RkLEdBQUcsQ0FBQ0ssTUFBTSxDQUFDLEdBQUcsQ0FBQyxDQUFDQyxJQUFJLENBQUM7b0JBQUVTLEVBQUUsRUFBRUYsTUFBTSxDQUFDRSxFQUFFO29CQUFFTixJQUFJO29CQUFFQyxLQUFLO2lCQUFFLENBQUM7WUFDdEQsRUFBRSxPQUFPSCxNQUFLLEVBQUU7Z0JBQ2RQLEdBQUcsQ0FBQ0ssTUFBTSxDQUFDLEdBQUcsQ0FBQyxDQUFDQyxJQUFJLENBQUM7b0JBQUVDLEtBQUssRUFBRUEsTUFBSyxDQUFDQyxPQUFPO2lCQUFFLENBQUM7WUFDaEQsQ0FBQztZQUNELE1BQUs7UUFFUDtZQUNFUixHQUFHLENBQUNLLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQ1csR0FBRyxFQUFFLENBQUMscUJBQXFCOztLQUM5QztBQUNILENBQUMiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9teS1uZXh0anMtYXBwLy4vcGFnZXMvYXBpL3VzZXJzL2luZGV4LmpzPzFkOGIiXSwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgb3BlbkRiIH0gZnJvbSAnLi4vLi4vLi4vbGliL2RiJ1xuXG5leHBvcnQgZGVmYXVsdCBhc3luYyBmdW5jdGlvbiBoYW5kbGVyKHJlcSwgcmVzKSB7XG4gIGNvbnN0IGRiID0gb3BlbkRiKClcblxuICBzd2l0Y2ggKHJlcS5tZXRob2QpIHtcbiAgICBjYXNlICdHRVQnOlxuICAgICAgdHJ5IHtcbiAgICAgICAgY29uc3QgdXNlcnMgPSBhd2FpdCBkYi5hbGwoJ1NFTEVDVCAqIEZST00gdXNlcnMnKVxuICAgICAgICByZXMuc3RhdHVzKDIwMCkuanNvbih1c2VycylcbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIHJlcy5zdGF0dXMoNTAwKS5qc29uKHsgZXJyb3I6IGVycm9yLm1lc3NhZ2UgfSlcbiAgICAgIH1cbiAgICAgIGJyZWFrXG5cbiAgICBjYXNlICdQT1NUJzpcbiAgICAgIGNvbnN0IHsgbmFtZSwgZW1haWwgfSA9IHJlcS5ib2R5XG4gICAgICB0cnkge1xuICAgICAgICAvLyDkv67mlLnov5nph4zvvJrkvb/nlKggZ2V0IOaWueazleadpeiOt+WPluaPkuWFpeeahCBJRFxuICAgICAgICBhd2FpdCBkYi5ydW4oXG4gICAgICAgICAgJ0lOU0VSVCBJTlRPIHVzZXJzIChuYW1lLCBlbWFpbCkgVkFMVUVTICg/LCA/KScsXG4gICAgICAgICAgW25hbWUsIGVtYWlsXVxuICAgICAgICApXG4gICAgICAgIGNvbnN0IHJlc3VsdCA9IGF3YWl0IGRiLmdldCgnU0VMRUNUIGxhc3RfaW5zZXJ0X3Jvd2lkKCkgYXMgaWQnKVxuICAgICAgICByZXMuc3RhdHVzKDIwMSkuanNvbih7IGlkOiByZXN1bHQuaWQsIG5hbWUsIGVtYWlsIH0pXG4gICAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgICByZXMuc3RhdHVzKDQwMCkuanNvbih7IGVycm9yOiBlcnJvci5tZXNzYWdlIH0pXG4gICAgICB9XG4gICAgICBicmVha1xuXG4gICAgZGVmYXVsdDpcbiAgICAgIHJlcy5zdGF0dXMoNDA1KS5lbmQoKSAvLyBNZXRob2QgTm90IEFsbG93ZWRcbiAgfVxufSJdLCJuYW1lcyI6WyJvcGVuRGIiLCJoYW5kbGVyIiwicmVxIiwicmVzIiwiZGIiLCJtZXRob2QiLCJ1c2VycyIsImFsbCIsInN0YXR1cyIsImpzb24iLCJlcnJvciIsIm1lc3NhZ2UiLCJuYW1lIiwiZW1haWwiLCJib2R5IiwicnVuIiwicmVzdWx0IiwiZ2V0IiwiaWQiLCJlbmQiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(api)/./pages/api/users/index.js\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/users/index.js"));
module.exports = __webpack_exports__;

})();