import { useContext, useEffect, useState } from 'react'
import style from './style.module.css'
import { Button, Popconfirm, Space, Table, message } from 'antd'
import { AuthContext } from '../../states/authState'
import { Navigate } from 'react-router-dom'
export default function Home() {
    const { userAuth, data,setData } = useContext(AuthContext)
    const [status, setStatus] = useState(0)
    const url = "http://localhost:5000/task"
    useEffect(() => {
        (async () => {
            try {
                const res = await fetch(url, {
                    headers: {
                        authorization: localStorage.getItem("token")
                    }
                })
                if (res.ok) {
                    const d = await res.json()
                    setData(d)
                }
                if (res.status == 304) {
                    message.warning("Something went wrong")
                }
                if (res.status == 500) {
                    message.error("Server error occured")
                }
            } catch (error) {
                message.error(error)
            }
        })()
    }, [])

    const updateStatus = async(task_id)=>{
        try {
            const res = await fetch(url+"?id="+task_id+"&status="+status,{
                method:"PATCH",
                headers:{
                    authorization:localStorage.getItem("token")
                }
            })
            if(res.ok){
                message.success("Status Updated")
                setData(p=>{
                    let newArr = [...p]
                    console.log(newArr);
                    const idx = p.findIndex(t=>t.task_id==task_id)
                    console.log("object",idx);
                    newArr[idx].status = status
                    console.log(newArr);
                    return newArr
                })
                return
            } 
            if(res.status==304){
                message.warning("Something went wrong")
                return
            }
            if(res.status==500){
                message.error("Internal server error")
                return
            }
        } catch (error) {
            message.error(error)
        }
    }

    const deleteTask = async(task_id)=>{
        try {
            const res = await fetch(url+"?id="+task_id,{
                method:"DELETE",
                headers:{
                    authorization:localStorage.getItem("token")
                }
            })
            if(res.ok){
                message.success("Task deleted")
                setData(p=>{
                    const newData = p.filter(task=>task.task_id!=task_id)
                    return newData
                })
                return
            } 
            if(res.status==304){
                message.warning("Something went wrong")
                return
            }
            if(res.status==500){
                message.error("Internal server error")
                return
            }
        } catch (error) {
            message.error(error)
        }
    }

    const cols = [
        {
            title: "Task",
            dataIndex: "task"
        },
        {
            title: "Description",
            dataIndex: "task_desc"
        },
        {
            title: "Due Date",
            dataIndex: "due"
        },
        {
            title: "Assignee",
            dataIndex: "assignee"
        },
        {
            title: "Status",
            dataIndex: "status",
            render: (sts, record) => {
                if (sts == 0)
                    return <span style={{ background: "grey", color: "white", padding: "2px 5px" }}>Not Started Yet</span>
                if (sts == 1)
                    return <span style={{ backgroundColor: "yellow", padding: "2px 5px", color: "grey" }}>In Progress</span>
                if (sts == 2)
                    return <span style={{ backgroundColor: "dodgerblue", color: "white", padding: "2px 5px" }}>Completed</span>
            }
        },
        {
            title: "Priority",
            dataIndex: "priority",
            render: (p, record) => {
                if (p.toLowerCase() == 'l')
                    return <span style={{ backgroundColor: "green", color: "white", padding: "2px 4px" }}>Low</span>
                if (p.toLowerCase() == 'm')
                    return <span style={{ backgroundColor: "orange", color: "white", padding: "2px 5px" }}>Medium</span>
                if (p.toLowerCase() == 'h')
                    return <span style={{ backgroundColor: "red", color: "white", padding: "2px 5px" }}>High</span>
            }
        },
        {
            title: "Created By",
            dataIndex: "createdBy",
            render: (c, record) => {
                if (c == null)
                    return "web scrapper"
                else
                    return record.u_id == userAuth.u_id ? "Me" : record.name
            }
        },
        {
            title: "Actions",
            dataIndex:"task_id",
            render: (id, record) => {
                return (
                    <Space>
                        <Popconfirm title="are you sure" onConfirm={e=>deleteTask(id)}>
                            <Button danger>Delete</Button>
                        </Popconfirm>
                        <Popconfirm title={
                            <div className={style.miniContext}>
                                <label htmlFor="">Select status: </label>
                                <select onInput={e=>setStatus(e.target.value)}>
                                    <option value="0">Not started</option>
                                    <option value="1">In progress</option>
                                    <option value="2">Completed</option>
                                </select>
                            </div>
                        } onConfirm={e=>updateStatus(id)}>
                            <Button type='primary'>Status Update</Button>
                        </Popconfirm>
                    </Space>
                )
            }
        }
    ]
    return (
        <>
            {
                console.log(status)
            }
            {
                userAuth.isLoggedIn
                    ? null : <Navigate to="/login" />
            }
            <Table
                dataSource={data}
                columns={cols}
            >

            </Table>
        </>
    )
}