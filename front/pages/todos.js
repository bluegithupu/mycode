// pages/todos.js
import { useEffect, useState } from 'react';
import styles from '../styles/Todos.module.css';

export default function TodosPage() {
    const [todos, setTodos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newTodo, setNewTodo] = useState({
        title: '',
        completed: false,
        userId: 1
    });

    // 获取数据
    const fetchTodos = async () => {
        try {
            const response = await fetch('https://jsonplaceholder.typicode.com/todos');
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            const data = await response.json();
            setTodos(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTodos();
    }, []);

    // 处理新增
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            setLoading(true);
            const response = await fetch('https://jsonplaceholder.typicode.com/todos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newTodo),
            });

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            // 重新获取最新数据
            await fetchTodos();

            // 关闭弹窗并重置表单
            setIsModalOpen(false);
            setNewTodo({ title: '', completed: false, userId: 1 });
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    // 加载状态
    if (loading) return <div className={styles.loading}>Loading...</div>;

    // 错误状态
    if (error) return <div className={styles.error}>Error: {error}</div>;

    // 渲染列表
    return (
        <div className={styles.container}>
            <div className={styles.header}>
                <h1>Todos List ({todos.length})</h1>
                <button
                    className={styles.addButton}
                    onClick={() => setIsModalOpen(true)}
                >
                    新增任务
                </button>
            </div>

            {/* 新增任务弹窗 */}
            {isModalOpen && (
                <div className={styles.modal}>
                    <div className={styles.modalContent}>
                        <h2>新增任务</h2>
                        <form onSubmit={handleSubmit}>
                            <div className={styles.formGroup}>
                                <label>标题：</label>
                                <input
                                    type="text"
                                    value={newTodo.title}
                                    onChange={(e) => setNewTodo({ ...newTodo, title: e.target.value })}
                                    required
                                />
                            </div>
                            <div className={styles.formGroup}>
                                <label>
                                    <input
                                        type="checkbox"
                                        checked={newTodo.completed}
                                        onChange={(e) => setNewTodo({ ...newTodo, completed: e.target.checked })}
                                    />
                                    已完成
                                </label>
                            </div>
                            <div className={styles.formActions}>
                                <button type="submit">保存</button>
                                <button type="button" onClick={() => setIsModalOpen(false)}>取消</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <table className={styles['todo-table']}>
                <thead>
                    <tr>
                        <th>状态</th>
                        <th>标题</th>
                        <th>用户ID</th>
                    </tr>
                </thead>
                <tbody>
                    {todos.map((todo) => (
                        <tr key={todo.id}>
                            <td>{todo.completed ? '✅' : '⏳'}</td>
                            <td>{todo.title}</td>
                            <td>{todo.userId}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}