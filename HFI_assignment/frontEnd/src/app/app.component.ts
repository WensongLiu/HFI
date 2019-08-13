import { Component, OnInit} from '@angular/core';
import { Router } from '@angular/router';
import { loginInfo } from './shared/classes/loginInfo';
import { member } from './shared/classes/member';
import { FormGroup, FormControl, FormBuilder, Validators } from '@angular/forms';
import { LoginService } from './shared/services/login.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],

  providers: [LoginService]
})
export class AppComponent implements OnInit{

  private loginInfo: loginInfo;
  private members: any;
  private member: member;
  private flag: Number;
  private loginInfoForm = this.fb.group({
    memberID: [''],
    fullName: ['']
  });
  

  constructor(private fb: FormBuilder, private router : Router, private loginService: LoginService) {
    this.loginService.array;
  }

  ngOnInit(){
  }

  async onLogin(){
    if(this.loginInfoForm.value.memberID == '' || this.loginInfoForm.value.fullName == '')
    {
      alert("All fields are required, please try again!");
    }
    else{
      this.loginInfo = new loginInfo(this.loginInfoForm.value.memberID, this.loginInfoForm.value.fullName);

      const promise = new Promise((resolve, reject) => {
        this.loginService.login(this.loginInfo)
          .then(
            res => { // Success  
              this.members = res.unsubscribe;
              console.log(this.members);
            },
          )
      });
      await promise;
    }
    this.toCheck();
  }

  toCheck(){
    if(this.loginService.flag == 200 || 299){
      this.router.navigate(['/summary'])
    }
    else alert('Wrong member ID or full name, please try again!')
  }
}
