const valid=()=>{
let user=document.getElementById("floatingInput").value;
let pass=document.getElementById("floatingPassword").value;
if(user!="akshay" || pass!=12345)
alert("invalid login credentials")
else
{
    window.location.href="admin_front";
}
};
