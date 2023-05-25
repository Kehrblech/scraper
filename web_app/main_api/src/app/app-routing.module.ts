import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GetCompComponent } from './get/get-comp/get-comp.component';

const routes: Routes = [
  {path:'get', component: GetCompComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
