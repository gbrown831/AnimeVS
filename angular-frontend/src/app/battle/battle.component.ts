import { Component, Output, EventEmitter, OnInit  } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-battle',
  standalone: true,
  imports: [],
  templateUrl: './battle.component.html',
  styleUrl: './battle.component.css'
})
export class BattleComponent {
  @Output() setView = new EventEmitter<boolean>();
  left!: string;
  right!: string;

  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

  ngOnInit() {
    this.getImages();
  }

  getImages() {

    axios.get('http://127.0.0.1:5000/Naruto_Uzumaki')
    .then((res) => {
      this.left = "https://static.wikia.nocookie.net/naruto/images/d/d6/Naruto_Part_I.png"
    })
    .catch((err) => console.log(err));
    axios.get('http://127.0.0.1:5000/Sasuke_Uchiha')
    .then((res) => {
      this.right = "https://static.wikia.nocookie.net/naruto/images/2/21/Sasuke_Part_1.png"
    })
    .catch((err) => console.log(err));

  }
}
