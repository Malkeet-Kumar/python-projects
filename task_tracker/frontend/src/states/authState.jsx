import React, { useState } from "react";
export const AuthContext = React.createContext()
export function AuthState(props){
    const [userAuth, setUserAuth] = useState({isLoggedIn:false,role:""})
    return(
        <AuthContext.Provider value={{userAuth,setUserAuth}}>
            {props.children}
        </AuthContext.Provider>
    )
}