# Week 1 — App Containerization


## Task 1: Create a Docker file on bakend-flask

Copy and paste this code in the docker file

```
  FROM python:3.10-slim-buster
  WORKDIR /backend-flask
  COPY requirements.txt requirements.txt
  RUN pip3 install -r requirements.txt
  COPY . .
  ENV FLASK_ENV=development
  EXPOSE ${PORT}
  CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
  
  ```

### On the CLI terminal Run:

⦁	pip3 install -r requirements.txt
It will install the python libraries use for the app.
### Run Docker CMD:
⦁	python3 -m flask run --host=0.0.0.0 --port=4567

Now make sure the backend port(4567) is unlock then click on the link and add these suffix at the end of the URL: /api/activities/home
now new backend URL will be like this:

https://4567-smbaig235-awsbootcampcr-vq3wfbapb9w.ws-us87.gitpod.io/api/activities/home 

Screenshot of the Backend page:

![Backendimage](weekly_images/Backend.jpg)


### Build Container
⦁	docker build -t  backend-flask ./backend-flask

### Display Container Image:
⦁	Docker image  

Now Set environment variable with these commands:
```
 set FRONTEND_URL="*"
 set BACKEND_URL="*"
```
### Overridding Ports:
⦁	 docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask

Now list the container from this docker command:
`docker ps`
Now change directory to: cd frontend-react-js/
then run npm Install before building the container,it needs to copy the contents of node_modules
	`npm i`

## Task 2: Create a Docker file on Frontend-react-js

copy and paste this code in the docker file
 
 ```
FROM node:16.18
ENV PORT=3000
COPY . /frontend-react-js
WORKDIR /frontend-react-js
RUN npm install
EXPOSE ${PORT}
CMD ["npm", "start"]
```
### Build Container
`docker build -t frontend-react-js ./frontend-react-js`
### Run Container
`docker run -p 3000:3000 -d frontend-react-js`

Now create a file on root project: "docker-compose.yml" then copy this code:

```
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js
networks: 
  internal-network:
    driver: bridge
    name: cruddur
```
then right click on compose.yaml & click on compose up OR run command:
  `docker compose up`
docker-compose up’ is a Docker command to start and run an entire app on a standalone host that contains multiple services.

Now make sure frontend port 3000 is unlock now click on the link

![Frontendimage](weekly_images/Frontend.jpg)

At the end Commit and synchronize all the changes done in the repository OR 
Run: git push.

## Task 3: Notification endpoint for the openAPI

 Step 1: first install  npm run " npm i "on frontend-react-js directory
then compose up the compose.yaml file to start up the environment.Click on the port 3000 so the both ends are communicating.
Step 2: we need to authenticate ourself on the site hit join now and enter some information to enter the app as the authenticated user.
Step 3: Open the openAPI library click on the elipsis & select add new api path then add the following code:

### backend-flask/openapi.yaml 

```
      /api/activities/notification:
    get:
      description: 'Return a feed of activity for all those I followers'
      tags:
      - activities
      parameters: []
      responses:
        '200':
        description: Returns an array of activities
        content:
        application/json:
        schema:
         type: array
         items:
         $ref: '#/components/schemas/Activity'
```


### Step 4: To add an endpoint backend-flask/app.py

Import from services.notifications_activities import *

also add this code in app.py file

```
@app.route("/api/activities/notifications", methods=['GET'])
def data_notification():
  data = NotificationActivities.run()
  return data, 200
```

Step 4: 
Now create a file in backend-flask: "notifications_activities.py" add the following code:

```
from datetime import datetime, timedelta, timezone
class NotificationActivities:
  def run():
    now = datetime.now(timezone.utc).astimezone()
    results = [{
      'uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
      'handle':  'xyz',
      'message': 'I like spring',
      'created_at': (now - timedelta(days=2)).isoformat(),
      'expires_at': (now + timedelta(days=5)).isoformat(),
      'likes_count': 5,
      'replies_count': 1,
      'reposts_count': 0,
      'replies': [{
        'uuid': '26e12864-1c26-5c3a-9658-97a10f8fea67',
        'reply_to_activity_uuid': '68f126b0-1ceb-4a33-88be-d90fa7109eee',
        'handle':  'Worf',
        'message': 'This post has no honor!',
        'likes_count': 0,
        'replies_count': 0,
        'reposts_count': 0,
        'created_at': (now - timedelta(days=2)).isoformat()
      }],
    }
    
    ]
    return results
```

## Task 4: Flask backend endpoint for notification  & React page for Notifications.

Step 1: goto the frontend-react-js directory/app.js

```
import './App.css';
import HomeFeedPage from './pages/HomeFeedPage';
import NotificationsFeedPage from './pages/NotificationsFeedPage ';
import UserFeedPage from './pages/UserFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import React from 'react';

import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom";

const router = createBrowserRouter([
{
    path: "/",
    element: <HomeFeedPage />
  },
  {
    path: "/notifications",
    element: <NotificationsFeedPage />
  },
  {
    path: "/@:handle",
    element: <UserFeedPage />
  },
  {
    path: "/messages",
    element: <MessageGroupsPage />
  },
  {
    path: "/messages/@:handle",
    element: <MessageGroupPage />
  },
  {
    path: "/signup",
    element: <SignupPage />
  },
  {
    path: "/signin",
    element: <SigninPage />
  },
  {
    path: "/confirm",
    element: <ConfirmationPage />
  },
  {
    path: "/forgot",
    element: <RecoverPage />
  }
]);

function App() {
  return (
    <>
      <RouterProvider router={router} />
    </>
  );
}

export default App;

```

Step 2: Now create two file under "pages" file name them : 

1.	NotificationsFeedPage.js 
2.	NotificationsFeedPage.css

 Now write the following code in  NotificationsFeedPage.js file
 
```
import './NotificationFeedPage.css';
import React from "react";

import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';

// [TODO] Authenication
import Cookies from 'js-cookie'

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/notifications`
      const res = await fetch(backend_url, {
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  const checkAuth = async () => {
    console.log('checkAuth')
    // [TODO] Authenication
    if (Cookies.get('user.logged_in')) {
      setUser({
        display_name: Cookies.get('user.name'),
        handle: Cookies.get('user.username')
      })
    }
  };

  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth();
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm  
          popped={popped}
          setPopped={setPopped} 
          setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} 
          popped={poppedReply} 
          setPopped={setPoppedReply} 
          setActivities={setActivities} 
          activities={activities} 
        />
        <ActivityFeed 
          title="Home" 
          setReplyActivity={setReplyActivity} 
          setPopped={setPoppedReply} 
          activities={activities} 
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}
```

Step 3: Now commit all the changes of implementation on frontend-reacr-js for notification page.Here is the screenshot of the page.
 
![Notifiactionimage](weekly_images/Notificationpage.jpg)

## Task 5: Run dynamoDB local Container & Run postgres Container.

Step 1: On the root directory open compose.yaml copy and paste this code:

```
  dynamodb-local:
    # https://stackoverflow.com/questions/67533058/persist-local-dynamodb-data-in-volumes-lack-permission-unable-to-open-databa
    # We needed to add user:root to get this working.
    user: root
    command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
    image: "amazon/dynamodb-local:latest"
    container_name: dynamodb-local
    ports:
      - "8000:8000"
    volumes:
      - "./docker/dynamodb:/home/dynamodblocal/data"
    working_dir: /home/dynamodblocal

 db:
    image: postgres:13-alpine
    restart: always
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - '5432:5432'
    volumes: 
      - db:/var/lib/postgresql/data
volumes:
  db:
    driver: local
```
Step 2: Now compose up the "compose.yaml" then open the required ports: 5432 , 4567 , 8000

### Create a table:
```
aws dynamodb create-table \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --attribute-definitions \
        AttributeName=Artist,AttributeType=S \
        AttributeName=SongTitle,AttributeType=S \
    --key-schema AttributeName=Artist,KeyType=HASH AttributeName=SongTitle,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --table-class STANDARD

![tableimage](weekly_images/Createtable.jpg)

```
### Create an item:

```
aws dynamodb put-item \
    --endpoint-url http://localhost:8000 \
    --table-name Music \
    --item \
        '{"Artist": {"S": "No One You Know"}, "SongTitle": {"S": "Call Me Today"}, "AlbumTitle": {"S": "Somewhat Famous"}}' \
    --return-consumed-capacity TOTAL
    
```

![Itemimage](weekly_images/Createitem.jpg)

### List table:
aws dynamodb list-tables --endpoint-url http://localhost:8000

![Listimage](weekly_images/Listtable.jpg)

### Get records:
aws dynamodb scan --table-name Music --query "Items" --endpoint-url http://localhost:8000

![Recordimage](weekly_images/Getrecords.jpg)


Step 3: goto gitpod.yaml paste this code:

   ```
  - name: postgres
    init: |
      curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
      echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
      sudo apt update
      sudo apt install -y postgresql-client-13 libpq-dev
   ```

Step 4: Run on the CLI terminal.

```
  curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
  echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list
  sudo apt update
  psql -Upostgres --host localhost
```




