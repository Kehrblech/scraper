import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SlideShowComponent } from './slideshow/slideshow.component';
import { StartPageComponent } from './start-page/start-page.component';

const routes: Routes = [
  {path: '', redirectTo: 'home', pathMatch: 'full' },
  {path:'home', component: StartPageComponent},
  {path:'slideshow', component: SlideShowComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
