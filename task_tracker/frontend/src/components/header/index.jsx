import { useContext, useState } from 'react'
import style from './style.module.css'
import { CgLogOut, CgProfile } from 'react-icons/cg'
import { MdAssignmentAdd } from 'react-icons/md'
import { AuthContext } from '../../states/authState'
import { Modal, message } from 'antd'

export default function Header() {
    const { userAuth, setUserAuth, setData } = useContext(AuthContext)
    const [modal,setModal] = useState(false)
    const [task,setTask]=useState("")
    const [desc,setDesc]=useState("")
    const [date,setDate]=useState("")
    const [assignee,setAssignee]=useState("")
    const [priority,setPriority]=useState("")

    const addTask =async()=>{
        try {
            const res = await fetch("http://localhost:5000/task",{
                method:"POST",
                headers:{
                    'content-type':'application/json',
                    'authorization':localStorage.getItem("token")
                },
                body:JSON.stringify({task,desc,date,assignee,priority})
            })
            const json = await res.json()
            if(res.status==200){
                setData(p=>{
                    console.log(p);
                    return [...p,json[0].task]
                })
                // console.log(json[0].task);
            }
            if(res.status==304){
                message.error("something went wrong")
            }
            if(res.status==500){
                message.error("Server error")
            }

            setModal(false)
        } catch (error) {
            console.log(error);
            message.error(error)
        }
    }

    return (
        <div className={style.header}>
            <div className={style.left}>
                <h2>Task tracker</h2>
            </div>
            <div className={style.right}>
                {
                    userAuth.isLoggedIn ?
                        <>
                            <span style={{marginRight:"10px",fontSize:"25px", display:'flex', alignItems:'center'}}><MdAssignmentAdd onClick={e=>setModal(p=>!p)}/></span>
                            <CgProfile style={{ fontSize: "25px" }} />
                            <span style={{ fontSize: "20px" }}>{userAuth?.name}</span>
                            <CgLogOut style={{ fontSize: "25px" }} onClick={e => {
                                localStorage.removeItem("token")
                                localStorage.removeItem("user")
                                setUserAuth(p => { return { isLoggedIn: false, role: "" } })
                            }} />
                        </> :
                        null
                }
            </div>
            <Modal title="Add task" onCancel={e=>{
                setModal(false)
            }} 
            onOk={e=>{
                addTask()
            }} 
            open={modal}>
                <div className={style.addTask}>
                    <label htmlFor="">Task :</label>
                    <input type="text" value={task} onInput={e=>{setTask(e.target.value)}} placeholder='Task Name'/>

                    <label htmlFor="">Descrition :</label>
                    <textarea name="" id="" cols="30" rows="3" placeholder='Descibe task...' value={desc} onInput={e=>setDesc(e.target.value)}></textarea>

                    <label htmlFor="">Date :</label>
                    <input type="date" onInput={e=>setDate(e.target.value)}/>

                    <label htmlFor="">Assignee :</label>
                    <input type="text" placeholder='Assignee' value={assignee} onInput={e=>setAssignee(e.target.value)} />

                    <label htmlFor="">Priority :</label>
                    <select onInput={e=>setPriority(e.target.value)}>
                        <option value="l">Low</option>
                        <option value="m">Medium</option>
                        <option value="h">High</option>
                    </select>
                </div>
            </Modal>
        </div>
    )
}