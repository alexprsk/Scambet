export default async function HandleLogin(data) {
  const body = new URLSearchParams();
  body.append('username', data.username);
  body.append('password', data.password);

  const response = await fetch('https://localhost:8000/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Login failed' }));
    throw new Error(error.detail);
  }

  const { access_token, user_id } = await response.json(); 
  document.cookie = `access_token=${access_token}; path=/`;

  return { access_token, user_id }; // 
}




export async function HandleRegistration(data) {

    try {
        const response = await fetch('https://localhost:8000/auth/sign-up', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error("Registration failed");
        }
        console.log(data)
        const resData = await response.json();
        console.log(resData)
        console.log("Sent payload:", {
            username: [...data]


        });

    } catch (error) {
        console.log(error.message)

    }
}


export  async function HandleLogout() {
    const cookies = document.cookie.split(";");
    
    // Iterate through all cookies and delete each one
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        // Set the cookie's expiry date to a past date to delete it
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
    }
    

  return "Cookie deleted "; 
}


export function getCookie(name) {
  const cookies = document.cookie.split('; ');
  for (const cookie of cookies) {
    const [key, value] = cookie.split('=');
    if (key === name) return value;
  }
  return null;
}