import React, { useState, useEffect} from 'react';

export function Navigation() {
  const [isAuth, setIsAuth] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('access_token') !== null) {
      setIsAuth(true);
    }
  }, [isAuth]);

  return (
    
    <div>
        {isAuth ? <p href="/">Home</p> : null}
        {isAuth ? <p ref="/logout">Logout</p>: <p href="/login">Login</p>}
    </div>
  );
}