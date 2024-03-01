import { useContext, useState } from 'react'
import style from './style.module.css'
import { AuthContext } from '../../states/authState'
import {message } from 'antd'
import { Navigate, useNavigate } from 'react-router-dom'
export default function Login(){
    const [user,setUser] = useState({username:"",password:""})
    const {userAuth, setUserAuth} = useContext(AuthContext)
    const navigate = useNavigate()
    const login = async()=>{
        if(user.username.length<4){
            message.warning("Enter username")
            return
        }
        if(user.password.length<4){
            message.warning("Enter password")
            return
        }
        try {
            const res = await fetch("http://localhost:5000/login",{
                method:"POST",
                headers:{
                    'content-type':'application/json'
                },
                body:JSON.stringify(user)
            })
            if(res.status==200){
                const data = await res.json()
                localStorage.setItem("user",JSON.stringify({...data.user, isLoggedIn:true}))
                localStorage.setItem("token",data.token)
                setUserAuth({...data.user, isLoggedIn:true})
                message.success("Logged in")
                navigate('/')
            } else if(res.status==401){
                message.error("Invaiid password")
            } else if(res.status==404){
                message.error("User not found")
            } else {
                message.error("Something went wrong")
            }
        } catch (error) {
            message.error(error)
        }
    }
    return(
        <div className={style.container}>
            {
                userAuth.isLoggedIn?
                <Navigate to="/" />:
                null
            }
            <div className={style.form}>
                <h1>Login</h1>
                <div>
                    <label htmlFor="">Username</label>
                    <input type="text" placeholder='username' value={user.username} onInput={e=>setUser(p=>{return {...p,username:e.target.value}})}/>
                </div>
                <div>
                    <label htmlFor="">Password</label>
                    <input type="password" placeholder='password' value={user.password} onInput={e=>setUser(p=>{return {...p,password:e.target.value}})}/>
                </div>
                <button onClick={login}>Login</button>
            </div>
        </div>
    )
}