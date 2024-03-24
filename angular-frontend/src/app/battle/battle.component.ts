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
  leftID!: string;
  rightID!: string;
  leftURL!: string;
  rightURL!: string;

  hasVoted: boolean = false;

  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

  ngOnInit() {
    this.getImages();
  }

  getImages() {
    axios.get('http://127.0.0.1:5000/Naruto_Uzumaki')
    .then((res) => {
      this.leftURL = res.data.images[0]
      console.log(res.data)
    })
    .catch((err) => console.log(err));
    axios.get('http://127.0.0.1:5000/Sasuke_Uchiha')
    .then((res) => {
      this.rightURL = res.data.images[0]
    })
    .catch((err) => console.log(err));
  }


  postVotes() {
    this.hasVoted = true;
  }
}
