# Week 3 — Decentralized Authentication
## Task 1: Create an AWS Cognito User Pool for user group through AWS Console.
![AWSCognitoimage](week3_images/CognitoUserpool.jpg)
## Task 2: Install & configure amplify client side library.
### Step 1: Make sure to change directory into frontend-react-js then run this command:
`npm i aws-amplify --save`
### Step 2: To configure amplify open frontend-react-js/app.py file & add the following code.
```
import { Amplify } from 'aws-amplify';

Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,
  "oauth": {},
  Auth: {
    region: process.env.REACT_APP_AWS_PROJECT_REGION,           
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,        
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID,  
  }
});
```
### Step 3: Set the environment variable in docker compose.yaml file
```
REACT_APP_AWS_USER_POOLS_ID:"xxxx"
REACT_APP_CLIENT_ID:"xxxx"
```
Now commit the code.
### Step 4: Open homefeedpage.js page and add this code.

`import { Auth } from 'aws-amplify';`

`const [user, setUser] = React.useState(null);`

```
// check if we are authenicated
const checkAuth = async () => {
  Auth.currentAuthenticatedUser({    
     // If set to true, this call will send a 
    // request to Cognito to get the latest user data
    bypassCache: false 
  })
  .then((user) => {
    console.log('user',user);
    return Auth.currentAuthenticatedUser()
  }).then((cognito_user) => {
      setUser({
        display_name: cognito_user.attributes.name,
        handle: cognito_user.attributes.preferred_username
      })
  })
  .catch((err) => console.log(err));
};
```
## Task 3: Implement custom signout page.
### Step 1: open profileinfo.js file add the following code for signout.
`import { Auth } from 'aws-amplify';`
```
const signOut = async () => {
  try {
      await Auth.signOut({ global: true });
      window.location.href = "/"
  } catch (error) {
      console.log('error signing out: ', error);
  }
}
```
## Task 4: implement custom signin page
### Step 1: Open sigin.js page.Paste this code 
`import { Auth } from 'aws-amplify';`
```
const onsubmit = async (event) => {
  setErrors('')
  event.preventDefault();
    Auth.signIn(email, password)
      .then(user => {
        localStorage.setItem("access_token", user.signInUserSession.accessToken.jwtToken)
        window.location.href = "/"
      })
      .catch(error => {  
         if (error.code == 'UserNotConfirmedException') {
           window.location.href = "/confirm"
       }
       setErrors(error.message)
       });
      return false
     }
```
`console.log('user',user)`
### Step 2: Compose up and test the app for signin process.It should show the invalid email and password.
![TestEmailimage](week3_images/TestSignin.jpg)

### Step 3: Now Create a user through AWS Console in cognito user pool to test the signin process.
![Userimage](week3_images/User1.jpg)
### Step 4: Open the cruddur web page and enter the  email address you provided for the user on user pool.Result will be sucessful signin.
![Signinimage](week3_images/SiginTest.jpg)
## Task 5: Implement custom signup page 
### Step 1: Open signup.js file and the following code for signup.
`import { Auth } from 'aws-amplify';`
```
const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
      const { user } = await Auth.signUp({
        username: email,
        password: password,
        attributes: {
            name: name,
            email: email,
            preferred_username: username,
        },
        autoSignIn: { // optional - enables auto sign in after user is confirmed
            enabled: true,
        }
      });
      console.log(user);
      window.location.href = `/confirm?email=${email}`
  } catch (error) {
      console.log(error);
      setErrors(error.message)
  }
  return false
}
```
![Signupimage](week3_images/SignupTest.jpg)
## Task 5: Implement custom confirmation page
 ### Step 1:   
 `import { Auth } from 'aws-amplify';`
```
const onsubmit = async (event) => {
  event.preventDefault();
  setErrors('')
  try {
    await Auth.confirmSignUp(email, code);
    window.location.href = "/"
  } catch (error) {
    setErrors(error.message)
  }
  return false
}
```
```
const resend_code = async (event) => {
  setErrors('')
  try {
    await Auth.resendSignUp(email);
    console.log('code resent successfully');
    setCodeSent(true)
  } catch (err) {
    // does not return a code
    // does cognito always return english
    // for this to be an okay match?
    console.log(err)
    if (err.message == 'Username cannot be empty'){
      setErrors("You need to provide an email in order to send Resend Activiation Code")   
    } else if (err.message == "Username/client id combination not found."){
      setErrors("Email is invalid or cannot be found.")   
    }
  }
}
```
### Step 2: Now test the signup page and confirm the email by recieving activation code on the email address.
![Confirmimage](week3_images/ConfirmEmail.jpg)
## Task 6: Implement custom recovery page 
### Step 1: Open recover page and paste this code.
`import { Auth } from 'aws-amplify';`
```
const onsubmit_send_code = async (event) => {
  event.preventDefault();
  setErrors('')
  Auth.forgotPassword(username)
  .then((data) => setFormState('confirm_code') )
  .catch((err) => setErrors(err.message) );
  return false
}
```
```
const onsubmit_confirm_code = async (event) => {
  event.preventDefault();
  setErrors('')
  if (password == passwordAgain){
    Auth.forgotPasswordSubmit(username, code, password)
    .then((data) => setFormState('success'))
    .catch((err) => setCognitoErrors(err.message) );
  } else {
    setErrors('Passwords do not match')
  }
  return false
}
```
### Step 2: Commit all the changes we made and compose up the docker compose.yaml file to test our app.
### Step 3:  Now test password reset page by recieving the code on your email and reset it sucessfully.
![Passwordimage](week3_images/PasswordReset.jpg)

![Passwordimage](week3_images/PassReset.jpg)

### Step 4: Go to the AWS Console cognito user pool and check the users status both showed as a confirmed users.As shown in the image below.

![Usersimage](week3_images/User2.jpg)

## Task 7: Worked on improving UI & implement CSS variables for Theme.

![UIimage](week3_images/UIimproved.jpg)

## Task 8: Implement Cognito JWT server side Verification.

### Step 1: Open "homefeedpage.js" and the following code for authenticating server side.

```
 const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`
      const res = await fetch(backend_url, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("access_token")}`
        },
      
        method: "GET"
      });
```
### Step 2: For adding CORS open "app.py" file & paste this code.

```
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)
```
### Step 3: Go to  "requirements.txt" file add this flask for Cognito.

 `Flask-AWSCognito`

Now chage directory into backend-flask and run this requirement package.

`pip install -r requirements.txt`


### Step 4: Set the environment variables in docker compose.yaml file.

`AWS_COGNITO_USER_POOL_ID: "xxxx"`

`AWS_COGNITO_USER_POOL_CLIENT_ID: "xxxxx"`
then compose up.

### Step 5: Create a folder under backend-flask/lib/cognito_jwt_token.py and add the following code.

```
HTTP_HEADER = "Authorization"
import time
import requests
from jose import jwk, jwt
from jose.exceptions import JOSEError
from jose.utils import base64url_decode

class FlaskAWSCognitoError(Exception):
  pass

class TokenVerifyError(Exception):
  pass

def extract_access_token(request_headers):
    access_token = None
    auth_header = request_headers.get("Authorization")
    if auth_header and " " in auth_header:
        _, access_token = auth_header.split()
    return access_token

class CognitoJwtToken:
    def __init__(self, user_pool_id, user_pool_client_id, region, request_client=None):
        self.region = region
        if not self.region:
            raise FlaskAWSCognitoError("No AWS region provided")
        self.user_pool_id = user_pool_id
        self.user_pool_client_id = user_pool_client_id
        self.claims = None
        if not request_client:
            self.request_client = requests.get
        else:
            self.request_client = request_client
        self._load_jwk_keys()

    def _load_jwk_keys(self):
        keys_url = f"https://cognito-idp.{self.region}.amazonaws.com/{self.user_pool_id}/.well-known/jwks.json"
        try:
            response = self.request_client(keys_url)
            self.jwk_keys = response.json()["keys"]
        except requests.exceptions.RequestException as e:
            raise FlaskAWSCognitoError(str(e)) from e

    @staticmethod
    def _extract_headers(token):
        try:
            headers = jwt.get_unverified_headers(token)
            return headers
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    def _find_pkey(self, headers):
        kid = headers["kid"]
        # search for the kid in the downloaded public keys
        key_index = -1
        for i in range(len(self.jwk_keys)):
            if kid == self.jwk_keys[i]["kid"]:
                key_index = i
                break
        if key_index == -1:
            raise TokenVerifyError("Public key not found in jwks.json")
        return self.jwk_keys[key_index]

    @staticmethod
    def _verify_signature(token, pkey_data):
        try:
            # construct the public key
            public_key = jwk.construct(pkey_data)
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e
        # get the last two sections of the token,
        # message and signature (encoded in base64)
        message, encoded_signature = str(token).rsplit(".", 1)
        # decode the signature
        decoded_signature = base64url_decode(encoded_signature.encode("utf-8"))
        # verify the signature
        if not public_key.verify(message.encode("utf8"), decoded_signature):
            raise TokenVerifyError("Signature verification failed")

    @staticmethod
    def _extract_claims(token):
        try:
            claims = jwt.get_unverified_claims(token)
            return claims
        except JOSEError as e:
            raise TokenVerifyError(str(e)) from e

    @staticmethod
    def _check_expiration(claims, current_time):
        if not current_time:
            current_time = time.time()
        if current_time > claims["exp"]:
            raise TokenVerifyError("Token is expired")  # probably another exception

    def _check_audience(self, claims):
        # and the Audience  (use claims['client_id'] if verifying an access token)
        audience = claims["aud"] if "aud" in claims else claims["client_id"]
        if audience != self.user_pool_client_id:
            raise TokenVerifyError("Token was not issued for this audience")

    def verify(self, token, current_time=None):
        """ https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py """
        if not token:
            raise TokenVerifyError("No token provided")

        headers = self._extract_headers(token)
        pkey_data = self._find_pkey(headers)
        self._verify_signature(token, pkey_data)

        claims = self._extract_claims(token)
        self._check_expiration(claims, current_time)
        self._check_audience(claims)

        self.claims = claims 
        return claims
```
### Step 6: Open "app.py" file add these libraries and code.

`import sys`

`from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError`

```
cognito_jwt_token = CognitoJwtToken(
user_pool_id=os.getenv("AWS_COGNITO_USER_POOL_ID"),
user_pool_client_id=os.getenv("AWS_COGNITO_USER_POOL_CLIENT_ID"),
region=os.getenv("AWS_DEFAULT_REGION")
)
```

```
@app.route("/api/activities/home", methods=['GET'])
@xray_recorder.capture('activities_home')
def data_home():
  data = HomeActivities.run()
access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verifyy(access_token)

    # Authenticated Request
    app.logger.debug("authenicated")
    app.logger.debug(claims)
    app.logger.debug(claims['username'])
    data = HomeActivities.run(cognito_user_id=claims['username'])
  except TokenVerifyError as e:

    # Unauthenticated Request
    app.logger.debug(e)
    app.logger.debug("unauthenicated")
    data = HomeActivities.run()
  return data, 200
```
### Step 7: Go to the "profileinfo.js" add this code.

```
 const signOut = async () => {
    try {
      await Auth.signOut({ global: true });
      window.location.href = "/"
      localStorage.removeItem("access_token")
  } catch (error) {
      console.log('error signing out: ', error);
  }
  }
```
### Step 8: Open "homeactivities.py" file and the following code.

`def run(cognito_user_id=None):`

```
 if cognito_user_id != None:
        extra_crud = {
          'uuid': 'xxxxxxxx',
          'handle':  'Success',
          'message': 'The Key to Sucess is to focus on goals,Not Obstacles',
          'created_at': (now - timedelta(hours=1)).isoformat(),
          'expires_at': (now + timedelta(hours=12)).isoformat(),
          'likes': 1042,
          'replies': []
        }
        results.insert(0,extra_crud)
```
Now commit the code and compose up and test the login to verify JWT token.

![JWTverifyimage](week3_images/JWTtoken.jpg)