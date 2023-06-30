import { Injectable  } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ApiService  {
  constructor(private http: HttpClient) { }
  getData(url: string) {
    return this.http.get('http://127.0.0.1:5000/auto/?url='+url+'&type=slide');
  }
  getUrl(phrase: string) {
    return this.http.get('http://127.0.0.1:5000/findurl/?text='+phrase);
  }

}
