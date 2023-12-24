import {useState} from "react";

const checkPermission = () => {
  if (!("Notification" in window)) {
    alert("This browser does not support desktop notification");
    throw new Error("This browser does not support desktop notification");
  }
}

async function requestNotificationPermission() {
  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    alert("You need to grant notification permission");
  }
  else{
    new Notification("Notification permission granted", {body: "You will now receive attack notifications"});
  }
}

checkPermission();

setInterval(() => {
  if (Notification.permission !== "granted") {
    return;
  }
  fetch('http://localhost:5000/getNotifications').then(response => response.json()).then(data => {
    data.forEach((notification: any) => {
      new Notification(notification["title"], {
        body: notification["body"]
      });
      console.log(notification)
    });
  })
}, 5000);



export default function NotificationsSender() {
  const [mode, setMode] = useState("");

  let action = <button onClick={
    async () => {
      await requestNotificationPermission();
      setMode(" ")
    }
  }>Request permission</button>;

  if (Notification.permission === "granted") {
    action = <>Permission granted</>;
  }

  return (
    <div>
      Notifications: {action} {mode}
    </div>
  )
}