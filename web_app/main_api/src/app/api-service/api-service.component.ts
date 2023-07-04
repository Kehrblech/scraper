import { Injectable  } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class ApiService  {
  constructor(private http: HttpClient) { }
  getData(url: string) {
    return this.http.get('https://www.scrapi.de/auto/?url='+url+'&type=slide');
  }
  getUrl(phrase: string) {
    return this.http.get('https://www.scrapi.de/findurl/?text='+phrase);
  }

}
