import { Injectable } from '@angular/core';
import { HttpClientModule, HttpClient, HttpResponse, HttpHeaders } from '@angular/common/http';
import { loginInfo } from '../classes/loginInfo';
import { member } from '../classes/member';
import { Observable, of, using, from } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})

export class LoginService {

  private member: member;
  public array: any;
  public flag: number;
  

  constructor(
    private http: HttpClient
  ) { }

  async login(loginInfo){
    console.log(loginInfo.fullName+" service");
    console.log(loginInfo.memberID+" service");
    return this.http.post(`https://localhost:5001/api/Server/login`,loginInfo, { observe: "response"})
            .subscribe(async response => {
              await console.log(response.status);
              console.log(response.body[0].memberID);
              //console.log(response.body);
              this.array = response.body;
              this.flag = response.status;
              console.log(this.array);
              console.log(this.array.length);
              return this.flag;
            }, err => {
              throw err;
            });
  };
}