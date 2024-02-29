import { useContext, useState } from 'react'
import style from './style.module.css'
import { AuthContext } from '../../states/authState'
export default function Login(){
    const [user,setUser] = useState({username:"",password:""})
    const {userAuth, setUserAuth} = useContext(AuthContext)
    const login = async()=>{
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
                localStorage.setItem("user",JSON.stringify(data.user))
                localStorage.setItem("token",data.token)
                setUserAuth(data.user)
                alert("logged in")
            } else if(res.status==401){
                alert("wrong password")
            } else if(res.status==404){
                alert("user not found")
            } else {
                alert("something went wrong")
            }
        } catch (error) {
            alert(error)
        }
    }
    return(
        <div className={style.container}>
            <div className={style.form}>
                <h2>Login</h2>
                <div>
                    <label htmlFor="">Username</label>
                    <input type="text" value={user.username} onInput={e=>setUser(p=>{return {...p,username:e.target.value}})}/>
                </div>
                <div>
                    <label htmlFor="">Password</label>
                    <input type="text" value={user.password} onInput={e=>setUser(p=>{return {...p,password:e.target.value}})}/>
                </div>
                <button onClick={login}>Login</button>
            </div>
        </div>
    )
}