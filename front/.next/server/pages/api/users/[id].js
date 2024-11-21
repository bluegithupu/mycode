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
exports.id = "pages/api/users/[id]";
exports.ids = ["pages/api/users/[id]"];
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

/***/ "(api)/./pages/api/users/[id].js":
/*!*********************************!*\
  !*** ./pages/api/users/[id].js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   \"default\": () => (/* binding */ handler)\n/* harmony export */ });\n/* harmony import */ var _lib_db__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../lib/db */ \"(api)/./lib/db.js\");\n\nasync function handler(req, res) {\n    const db = (0,_lib_db__WEBPACK_IMPORTED_MODULE_0__.openDb)();\n    const { id  } = req.query;\n    switch(req.method){\n        case \"GET\":\n            try {\n                const user = await db.get(\"SELECT * FROM users WHERE id = ?\", [\n                    id\n                ]);\n                if (user) {\n                    res.status(200).json(user);\n                } else {\n                    res.status(404).json({\n                        message: \"用户未找到\"\n                    });\n                }\n            } catch (error) {\n                res.status(500).json({\n                    error: error.message\n                });\n            }\n            break;\n        case \"PUT\":\n            const { name , email  } = req.body;\n            try {\n                await db.run(\"UPDATE users SET name = ?, email = ? WHERE id = ?\", [\n                    name,\n                    email,\n                    id\n                ]);\n                res.status(200).json({\n                    id,\n                    name,\n                    email\n                });\n            } catch (error1) {\n                res.status(400).json({\n                    error: error1.message\n                });\n            }\n            break;\n        case \"DELETE\":\n            try {\n                await db.run(\"DELETE FROM users WHERE id = ?\", [\n                    id\n                ]);\n                res.status(200).json({\n                    message: \"用户已删除\"\n                });\n            } catch (error2) {\n                res.status(500).json({\n                    error: error2.message\n                });\n            }\n            break;\n        default:\n            res.status(405).end() // Method Not Allowed\n            ;\n    }\n}\n//# sourceURL=[module]\n//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiKGFwaSkvLi9wYWdlcy9hcGkvdXNlcnMvW2lkXS5qcy5qcyIsIm1hcHBpbmdzIjoiOzs7OztBQUF3QztBQUV6QixlQUFlQyxPQUFPLENBQUNDLEdBQUcsRUFBRUMsR0FBRyxFQUFFO0lBQzlDLE1BQU1DLEVBQUUsR0FBR0osK0NBQU0sRUFBRTtJQUNuQixNQUFNLEVBQUVLLEVBQUUsR0FBRSxHQUFHSCxHQUFHLENBQUNJLEtBQUs7SUFFeEIsT0FBUUosR0FBRyxDQUFDSyxNQUFNO1FBQ2hCLEtBQUssS0FBSztZQUNSLElBQUk7Z0JBQ0YsTUFBTUMsSUFBSSxHQUFHLE1BQU1KLEVBQUUsQ0FBQ0ssR0FBRyxDQUFDLGtDQUFrQyxFQUFFO29CQUFDSixFQUFFO2lCQUFDLENBQUM7Z0JBQ25FLElBQUlHLElBQUksRUFBRTtvQkFDUkwsR0FBRyxDQUFDTyxNQUFNLENBQUMsR0FBRyxDQUFDLENBQUNDLElBQUksQ0FBQ0gsSUFBSSxDQUFDO2dCQUM1QixPQUFPO29CQUNMTCxHQUFHLENBQUNPLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQ0MsSUFBSSxDQUFDO3dCQUFFQyxPQUFPLEVBQUUsT0FBTztxQkFBRSxDQUFDO2dCQUM1QyxDQUFDO1lBQ0gsRUFBRSxPQUFPQyxLQUFLLEVBQUU7Z0JBQ2RWLEdBQUcsQ0FBQ08sTUFBTSxDQUFDLEdBQUcsQ0FBQyxDQUFDQyxJQUFJLENBQUM7b0JBQUVFLEtBQUssRUFBRUEsS0FBSyxDQUFDRCxPQUFPO2lCQUFFLENBQUM7WUFDaEQsQ0FBQztZQUNELE1BQUs7UUFFUCxLQUFLLEtBQUs7WUFDUixNQUFNLEVBQUVFLElBQUksR0FBRUMsS0FBSyxHQUFFLEdBQUdiLEdBQUcsQ0FBQ2MsSUFBSTtZQUNoQyxJQUFJO2dCQUNGLE1BQU1aLEVBQUUsQ0FBQ2EsR0FBRyxDQUNWLG1EQUFtRCxFQUNuRDtvQkFBQ0gsSUFBSTtvQkFBRUMsS0FBSztvQkFBRVYsRUFBRTtpQkFBQyxDQUNsQjtnQkFDREYsR0FBRyxDQUFDTyxNQUFNLENBQUMsR0FBRyxDQUFDLENBQUNDLElBQUksQ0FBQztvQkFBRU4sRUFBRTtvQkFBRVMsSUFBSTtvQkFBRUMsS0FBSztpQkFBRSxDQUFDO1lBQzNDLEVBQUUsT0FBT0YsTUFBSyxFQUFFO2dCQUNkVixHQUFHLENBQUNPLE1BQU0sQ0FBQyxHQUFHLENBQUMsQ0FBQ0MsSUFBSSxDQUFDO29CQUFFRSxLQUFLLEVBQUVBLE1BQUssQ0FBQ0QsT0FBTztpQkFBRSxDQUFDO1lBQ2hELENBQUM7WUFDRCxNQUFLO1FBRVAsS0FBSyxRQUFRO1lBQ1gsSUFBSTtnQkFDRixNQUFNUixFQUFFLENBQUNhLEdBQUcsQ0FBQyxnQ0FBZ0MsRUFBRTtvQkFBQ1osRUFBRTtpQkFBQyxDQUFDO2dCQUNwREYsR0FBRyxDQUFDTyxNQUFNLENBQUMsR0FBRyxDQUFDLENBQUNDLElBQUksQ0FBQztvQkFBRUMsT0FBTyxFQUFFLE9BQU87aUJBQUUsQ0FBQztZQUM1QyxFQUFFLE9BQU9DLE1BQUssRUFBRTtnQkFDZFYsR0FBRyxDQUFDTyxNQUFNLENBQUMsR0FBRyxDQUFDLENBQUNDLElBQUksQ0FBQztvQkFBRUUsS0FBSyxFQUFFQSxNQUFLLENBQUNELE9BQU87aUJBQUUsQ0FBQztZQUNoRCxDQUFDO1lBQ0QsTUFBSztRQUVQO1lBQ0VULEdBQUcsQ0FBQ08sTUFBTSxDQUFDLEdBQUcsQ0FBQyxDQUFDUSxHQUFHLEVBQUUsQ0FBQyxxQkFBcUI7O0tBQzlDO0FBQ0gsQ0FBQyIsInNvdXJjZXMiOlsid2VicGFjazovL215LW5leHRqcy1hcHAvLi9wYWdlcy9hcGkvdXNlcnMvW2lkXS5qcz9hZWRkIl0sInNvdXJjZXNDb250ZW50IjpbImltcG9ydCB7IG9wZW5EYiB9IGZyb20gJy4uLy4uLy4uL2xpYi9kYidcblxuZXhwb3J0IGRlZmF1bHQgYXN5bmMgZnVuY3Rpb24gaGFuZGxlcihyZXEsIHJlcykge1xuICBjb25zdCBkYiA9IG9wZW5EYigpXG4gIGNvbnN0IHsgaWQgfSA9IHJlcS5xdWVyeVxuXG4gIHN3aXRjaCAocmVxLm1ldGhvZCkge1xuICAgIGNhc2UgJ0dFVCc6XG4gICAgICB0cnkge1xuICAgICAgICBjb25zdCB1c2VyID0gYXdhaXQgZGIuZ2V0KCdTRUxFQ1QgKiBGUk9NIHVzZXJzIFdIRVJFIGlkID0gPycsIFtpZF0pXG4gICAgICAgIGlmICh1c2VyKSB7XG4gICAgICAgICAgcmVzLnN0YXR1cygyMDApLmpzb24odXNlcilcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICByZXMuc3RhdHVzKDQwNCkuanNvbih7IG1lc3NhZ2U6ICfnlKjmiLfmnKrmib7liLAnIH0pXG4gICAgICAgIH1cbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIHJlcy5zdGF0dXMoNTAwKS5qc29uKHsgZXJyb3I6IGVycm9yLm1lc3NhZ2UgfSlcbiAgICAgIH1cbiAgICAgIGJyZWFrXG5cbiAgICBjYXNlICdQVVQnOlxuICAgICAgY29uc3QgeyBuYW1lLCBlbWFpbCB9ID0gcmVxLmJvZHlcbiAgICAgIHRyeSB7XG4gICAgICAgIGF3YWl0IGRiLnJ1bihcbiAgICAgICAgICAnVVBEQVRFIHVzZXJzIFNFVCBuYW1lID0gPywgZW1haWwgPSA/IFdIRVJFIGlkID0gPycsXG4gICAgICAgICAgW25hbWUsIGVtYWlsLCBpZF1cbiAgICAgICAgKVxuICAgICAgICByZXMuc3RhdHVzKDIwMCkuanNvbih7IGlkLCBuYW1lLCBlbWFpbCB9KVxuICAgICAgfSBjYXRjaCAoZXJyb3IpIHtcbiAgICAgICAgcmVzLnN0YXR1cyg0MDApLmpzb24oeyBlcnJvcjogZXJyb3IubWVzc2FnZSB9KVxuICAgICAgfVxuICAgICAgYnJlYWtcblxuICAgIGNhc2UgJ0RFTEVURSc6XG4gICAgICB0cnkge1xuICAgICAgICBhd2FpdCBkYi5ydW4oJ0RFTEVURSBGUk9NIHVzZXJzIFdIRVJFIGlkID0gPycsIFtpZF0pXG4gICAgICAgIHJlcy5zdGF0dXMoMjAwKS5qc29uKHsgbWVzc2FnZTogJ+eUqOaIt+W3suWIoOmZpCcgfSlcbiAgICAgIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgICAgIHJlcy5zdGF0dXMoNTAwKS5qc29uKHsgZXJyb3I6IGVycm9yLm1lc3NhZ2UgfSlcbiAgICAgIH1cbiAgICAgIGJyZWFrXG5cbiAgICBkZWZhdWx0OlxuICAgICAgcmVzLnN0YXR1cyg0MDUpLmVuZCgpIC8vIE1ldGhvZCBOb3QgQWxsb3dlZFxuICB9XG59Il0sIm5hbWVzIjpbIm9wZW5EYiIsImhhbmRsZXIiLCJyZXEiLCJyZXMiLCJkYiIsImlkIiwicXVlcnkiLCJtZXRob2QiLCJ1c2VyIiwiZ2V0Iiwic3RhdHVzIiwianNvbiIsIm1lc3NhZ2UiLCJlcnJvciIsIm5hbWUiLCJlbWFpbCIsImJvZHkiLCJydW4iLCJlbmQiXSwic291cmNlUm9vdCI6IiJ9\n//# sourceURL=webpack-internal:///(api)/./pages/api/users/[id].js\n");

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../../../webpack-api-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(api)/./pages/api/users/[id].js"));
module.exports = __webpack_exports__;

})();