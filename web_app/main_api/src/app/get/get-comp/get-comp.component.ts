import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';


@Component({
  selector: 'app-get-comp',
  templateUrl: './get-comp.component.html',
  styleUrls: ['./get-comp.component.css']
})
export class GetCompComponent {
  checkoutForm = this.formBuilder.group({
    inventory: null,
    price: null,
    productId: null,
    color: '',
    productName:'',
  });

  constructor(private http: HttpClient,
    private formBuilder: FormBuilder) { }

  onSubmit(): void {
    // Process checkout data here
    // Fehlerabfangen noch
    console.warn('Your order has been submitted', this.checkoutForm.value);
    let formObj = this.checkoutForm.getRawValue();



  }

}
