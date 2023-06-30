import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NavbarComponent } from './navbar/navbar.component';
import { MainComponent } from './main/main.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { InputBarComponent } from './main/input-bar/input-bar.component';
import { LandingpageComponent } from './landingpage/landingpage.component';
import { LayoutModule } from './layout/layout.module';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatButtonModule } from '@angular/material/button';
import { GetModule } from './get/get.module';
import { SlideShowComponent } from './slideshow/slideshow.component';
import { SlideComponent } from './slide/slide.component';
import { ApiService } from './api-service/api-service.component';
import { StartPageComponent } from './start-page/start-page.component';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatInputModule} from '@angular/material/input';
import {MatCardModule} from '@angular/material/card';
import {MatIconModule} from '@angular/material/icon';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    MainComponent,
    InputBarComponent,
    LandingpageComponent,
    SlideShowComponent,
    SlideComponent,
    StartPageComponent,

  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatFormFieldModule,
    FormsModule,
    HttpClientModule,
    LayoutModule,
    MatSidenavModule,
    MatButtonModule,
    GetModule,
    MatSnackBarModule,
    MatInputModule,
    MatCardModule,
    MatIconModule
  ],
  exports:[
    MatButtonModule
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
