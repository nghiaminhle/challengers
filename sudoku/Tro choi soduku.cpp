// Tro choi soduku.cpp : Defines the entry point for the console application.
// 2008

#include "stdafx.h"
#include <conio.h>

int  a[10][10],y[82],i,j,n;
bool b[10][10],d[10][10],c[10][10],o[10][10];
void rakq();
void tim(int i);
//////////////////////////////////////////////////////////////////////////
void rakq()
{ int j;
   
    for(i=1;i<=9;i++)
	{ 
	  for(j=1;j<=9;j++) 
	  { printf("%3d",a[i][j]);
	    if((j==3)||(j==6)) printf(" ");
	  }
	  printf("\n");
	  if((i==3)||(i==6))   printf("\n");
	};
	  n++;
};
//////////////////////////////////////////////////////////////////////////
void tim (int i)
{ int j,k,l;
  
  if(n==0) 
  {if(i%9==0) k=i/9;
   else k=i/9 +1;
   if   (i%9!=0) l=i%9;
   else l=9;
    
   if(i>81) rakq();
    else
	{  
	  if(b[k][l]==true)tim(i+1);
	  else
	  {for(j=1;j<=9;j++)
	   if((d[k][j]==false)&&(c[l][j]==false)&&(o[y[i]][j]==false))
	   {  a[k][l]=j;
		  d[k][j]=true;
		  c[l][j]=true;
		  o[y[i]][j]=true;
		  tim(i+1);
		  d[k][j]=false;
		  c[l][j]=false;
		  o[y[i]][j]=false; 
	   };
	  };
	};
  };
};
//////////////////////////////////////////////////////////////////////////
main()
{ int x,var,k,l;
  char ch;
     for(i=1;i<=9;i++)
	   for(j=1;j<=9;j++)
	   { 
		  // Manh Logic de xac dinh xem da dien chua
		 b[i][j]=false;
		 
		 // Mang Logic de xac dinhj xem dong da dien chua
         d[i][j]=false;
		 
		 // Mang Logic de xac dinh xem cot da dien chua
         c[i][j]=false;
		 
		 // Mang Logi de xac dinh xem o da dien chua/
         o[i][j]=false;
	   }; 
     //nhap so lieu.
	printf("\n nhap du lieu cho ma tran");
	printf("\n nhan phim 'e' neu khong muon nhap tiep: ");
	 for(i=1;i<=81;i++)
	 {if(i%9==0) k=i/9;
      else k=i/9 +1;
      if   (i%9!=0) l=i%9;
      else l=9;
      // Xac dinh o voi moi gia tri i tuong ung.
      if((k>0)&&(k<=3)&&(l>0)&&(l<=3)) y[i]=1;                               
      if((k>0)&&(k<=3)&&(l>3)&&(l<=6)) y[i]=2;
      if((k>0)&&(k<=3)&&(l>6)&&(l<=9)) y[i]=3;
      if((k>3)&&(k<=6)&&(l>0)&&(l<=3)) y[i]=4;
      if((k>3)&&(k<=6)&&(l>3)&&(l<=6)) y[i]=5;
      if((k>3)&&(k<=6)&&(l>6)&&(l<=9)) y[i]=6;
      if((k>6)&&(k<=9)&&(l>0)&&(l<=3)) y[i]=7;
      if((k>6)&&(k<=9)&&(l>3)&&(l<=6)) y[i]=8;
      if((k>6)&&(k<=9)&&(l>6)&&(l<=9)) y[i]=9;
	 }

	 do
	 { 
	  do
	  { printf("\n dong:");   scanf("%d",&k);
	  } while((k<=0)||(k>9));
	  do 
	  { printf("\n  cot:");   scanf("%d",&l);
	  } while((l<=0)||(l>9));
	  do
	  { printf("\n gia tri:");scanf("%d",&var);
	  } while((var<=0)||(var>9));
	   // Xac dinh o thoe bien x.
	   if((k>0)&&(k<=3)&&(l>0)&&(l<=3)) x=1;
       if((k>0)&&(k<=3)&&(l>3)&&(l<=6)) x=2;
       if((k>0)&&(k<=3)&&(l>6)&&(l<=9)) x=3;
       if((k>3)&&(k<=6)&&(l>0)&&(l<=3)) x=4;
       if((k>3)&&(k<=6)&&(l>3)&&(l<=6)) x=5;
       if((k>3)&&(k<=6)&&(l>6)&&(l<=9)) x=6;
       if((k>6)&&(k<=9)&&(l>0)&&(l<=3)) x=7;
       if((k>6)&&(k<=9)&&(l>3)&&(l<=6)) x=8;
       if((k>6)&&(k<=9)&&(l>6)&&(l<=9)) x=9;
       
	   a[k][l]=var;
	   b[k][l]=true;
	   d[k][var]=true;
	   c[l][var]=true;
	   o[x][var]=true;
	   
	   fflush(stdin);
	   ch=getchar();
	 }while(ch!='e');
     
	 n=0;
	 printf("\n");
	 tim(1);
    
     getch();
     return 0;
}
